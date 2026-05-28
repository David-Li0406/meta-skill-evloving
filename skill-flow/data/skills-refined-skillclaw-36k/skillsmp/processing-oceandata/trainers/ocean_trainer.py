import os
import torch
import logging
import numpy as np
import signal
from tqdm import tqdm
from einops import repeat

from .base import BaseTrainer
from utils import LossRecord
from utils.metrics import METRIC_DICT, VALID_METRICS


class OceanTrainer(BaseTrainer):
    """Trainer for ocean velocity prediction task"""

    def __init__(self, args):
        super().__init__(args)

        self.dataset = None # Store dataset for visualization

        for dataset_name, dataset_obj in [('train', self.train_loader.dataset),
                                            ('valid', self.valid_loader.dataset),
                                            ('test', self.test_loader.dataset)]:
            if hasattr(dataset_obj, 'dataset'):
                parent = dataset_obj.dataset
                if hasattr(parent, 'mask'):
                    self.mask = parent.mask
                    self.lat = parent.lat
                    self.lon = parent.lon
                    self.dataset = parent
                    break

        # Load model if model_path is provided
        self.start_epoch = 0
        model_path = args.get('model_path', None)
        if model_path is not None and os.path.exists(model_path):
            self._load_model(model_path)
            self.logger.info(f"Loaded model from {model_path}")

    def _load_model(self, model_path):
        """Load model from checkpoint file

        Args:
            model_path: Path to model file (.pth)
        """
        if isinstance(self.device, int):
          map_location = f'cuda:{self.device}'
        elif self.device == 'cpu':
            map_location = 'cpu'
        else:
            map_location = self.device

        checkpoint = torch.load(model_path, map_location=map_location)

        # Handle different checkpoint formats
        if isinstance(checkpoint, dict):
            if 'model_state_dict' in checkpoint:
                # Format: {'epoch': ..., 'model_state_dict': ..., 'optimizer_state_dict': ..., ...}
                self.model.load_state_dict(checkpoint['model_state_dict'])

                # Load optimizer state if available and in train mode
                if 'optimizer_state_dict' in checkpoint and self.args.get('mode', 'train') == 'train':
                    self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
                    self.logger.info("Loaded optimizer state for continued training")

                # Set start epoch if available
                if 'epoch' in checkpoint:
                    self.start_epoch = checkpoint['epoch'] + 1
                    self.logger.info(f"Resuming from epoch {self.start_epoch}")
            else:
                self.model.load_state_dict(checkpoint)
        else:
            self.model.load_state_dict(checkpoint)

    def _apply_mask_and_compute_loss(self, y_pred, y, patch_idx):
        """Apply per-region mask and compute loss (only on ocean pixels)

        Args:
            y_pred: (B, T_out, C, H, W) - predictions
            y: (B, T_out, C, H, W) - targets
            patch_idx: (B,) - region indices

        Returns:
            loss: scalar - MSE loss computed only on ocean pixels
            mae: scalar - MAE computed only on ocean pixels (or None)
        """

        if hasattr(self.dataset, 'mask_per_region') and self.dataset.mask_per_region is not None:
            # Get masks for this batch: (B, H, W) - True for land, False for ocean
            batch_masks = self.dataset.mask_per_region[patch_idx]
            # Convert to ocean mask: True for ocean, False for land
            ocean_mask = torch.from_numpy(~batch_masks).to(self.device).float()  # (B, H, W)
            # Expand to match prediction shape: (B, H, W) -> (B, T_out, C, H, W)
            ocean_mask = repeat(ocean_mask, 'b h w -> b t c h w',
                              t=y_pred.shape[1], c=y_pred.shape[2])

            # MSE loss: only divide by ocean pixels
            squared_error = (y_pred - y) ** 2 * ocean_mask
            mse_loss = squared_error.sum() / (ocean_mask.sum() + 1e-8)

            # MAE: optional
            abs_error = torch.abs(y_pred - y) * ocean_mask
            mae = abs_error.sum() / (ocean_mask.sum() + 1e-8)

            return mse_loss, mae, ocean_mask
        else:
            # No mask - use all pixels
            mse_loss = torch.nn.functional.mse_loss(y_pred, y)
            mae = torch.nn.functional.l1_loss(y_pred, y)
            return mse_loss, mae, None

    def train(self, epoch):
        """Train for one epoch with proper per-region mask handling"""
        loss_record = LossRecord(["train_loss"])
        self.model.train()

        pbar = tqdm(self.train_loader, desc=f"Epoch {epoch}")
        for batch_idx, batch_data in enumerate(pbar):
            # Unpack batch data
            if len(batch_data) == 3:
                x, y, patch_idx = batch_data
                patch_idx = patch_idx.numpy()  # (B,)
            else:
                raise ValueError("Batch data must include patch_idx. Check dataset implementation.")

            x = x.to(self.device)
            y = y.to(self.device)

            y_pred = self.model(x)  # (B, T_out, C, H, W)
            loss, _, _ = self._apply_mask_and_compute_loss(y_pred, y, patch_idx)

            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

            loss_record.update({"train_loss": loss.item()}, n=1)
            pbar.set_postfix({'loss': f'{loss.item():.2e}', 'avg': f'{loss_record.loss_dict["train_loss"].avg:.2e}'})

        # Note: ReduceLROnPlateau needs validation loss, so it's handled in process()
        # Other schedulers step at the end of each epoch
        if self.scheduler is not None and not isinstance(self.scheduler, torch.optim.lr_scheduler.ReduceLROnPlateau):
            self.scheduler.step()

        return loss_record

    def predict(self, x):
        """Make predictions and return both normalized and denormalized results"""
        self.model.eval()
        with torch.no_grad():
            x = x.to(self.device)
            y_pred_norm = self.model(x)

            if self.dataset is not None and hasattr(self.dataset, 'denormalize_data'):
                y_pred_real = self.dataset.denormalize_data(y_pred_norm)
            else:
                y_pred_real = y_pred_norm

        return y_pred_norm, y_pred_real

    def evaluate(self, split="valid", return_predictions=False, save_predictions=False):
        """Evaluate on validation or test set using real (denormalized) data with proper mask handling
        Args:
            split: 'valid' or 'test'
        Returns:
            loss_record: LossRecord object
            predictions_data: dict with all predictions (only if return_predictions=True)
        """
        metric_names = [f"{split}_loss"]  # Loss for progress tracking

        # All metrics computed from global data
        for metric in VALID_METRICS:
            metric_names.append(f"{split}_{metric}")

        loss_record = LossRecord(metric_names)
        self.model.eval()

        eval_loader = self.valid_loader if split == "valid" else self.test_loader

        # Store all predictions and targets for metric calculation -> (N*c*h*w, )
        all_predictions = []
        all_targets = []

        # Store full batch data if needed for saving -> Orginal shape
        if return_predictions:
            all_inputs = []
            all_predictions_full = []
            all_targets_full = []
            all_patch_indices = []

        with torch.no_grad():
            for batch_data in tqdm(eval_loader, desc=f"Eval {split}"):
                if len(batch_data) == 3:
                    x, y, patch_idx = batch_data
                    patch_idx = patch_idx.numpy()  # (B,)
                else:
                    raise ValueError("Batch data must include patch_idx. Check dataset implementation.")

                x = x.to(self.device)
                y = y.to(self.device)

                # Get both normalized and real predictions
                _, y_pred_real = self.predict(x)

                # Denormalize targets to get real values
                if self.dataset is not None and hasattr(self.dataset, 'denormalize_data'):
                    y_real = self.dataset.denormalize_data(y)
                else:
                    y_real = y

                # Store full batch data if needed
                if return_predictions:
                    all_inputs.append(x.cpu().numpy())
                    all_predictions_full.append(y_pred_real.cpu().numpy())
                    all_targets_full.append(y_real.cpu().numpy())
                    all_patch_indices.append(patch_idx)

                # Use the unified mask application method
                loss, mae, ocean_mask = self._apply_mask_and_compute_loss(y_pred_real, y_real, patch_idx)

                # Extract ocean pixels for metrics calculation
                if ocean_mask is not None:
                    masked_pred = y_pred_real[ocean_mask.bool()].cpu().numpy()
                    masked_target = y_real[ocean_mask.bool()].cpu().numpy()
                else:
                    masked_pred = y_pred_real.cpu().numpy().reshape(-1)
                    masked_target = y_real.cpu().numpy().reshape(-1)

                # Accumulate for global metrics
                all_predictions.extend(masked_pred)
                all_targets.extend(masked_target)

                # Only track loss for progress monitoring (not used in final metrics)
                loss_record.update({
                    f"{split}_loss": loss.item(),
                }, n=1)

        # Calculate all metrics using global accumulated data
        if len(all_predictions) > 0:
            all_predictions = np.array(all_predictions)
            all_targets = np.array(all_targets)

            # Compute all metrics from global data
            for metric_name in VALID_METRICS:
                try:
                    metric_func = METRIC_DICT[metric_name]
                    metric_value = metric_func(all_targets, all_predictions)
                    loss_record.update({f"{split}_{metric_name}": metric_value}, n=1)
                except Exception as e:
                    self.logger.warning(f"Failed to calculate {metric_name}: {e}")
                    loss_record.update({f"{split}_{metric_name}": float('nan')}, n=1)

        self.logger.info(f"[yingfanqaq]{split.capitalize()} |{loss_record}")

        if return_predictions:
            predictions_data = {
                'inputs': np.concatenate(all_inputs, axis=0),
                'predictions': np.concatenate(all_predictions_full, axis=0),
                'targets': np.concatenate(all_targets_full, axis=0),
                'patch_indices': np.concatenate(all_patch_indices, axis=0)
            }
            if save_predictions:
                self._save_predictions(predictions_data, split)

            return loss_record, predictions_data
        else:
            if save_predictions:
                assert "you must set the save_predictions=True"

        return loss_record

    def process(self):
        """Main training loop"""
        import time
        self.args['start_time'] = time.time()  # Record training start time

        self.logger.info("=" * 80)
        self.logger.info("Starting Training")
        self.logger.info(f"Epochs: {self.epochs} | Eval Freq: {self.eval_freq} | Patience: {self.patience}")
        if self.start_epoch > 0:
            self.logger.info(f"Resuming from epoch {self.start_epoch}")
        self.logger.info("=" * 80)

        # 设置退出标志
        interrupted = [False]
        
        def signal_handler(sig, frame):
            """处理Ctrl+C信号"""
            if not interrupted[0]:
                self.logger.info("\n" + "=" * 80)
                self.logger.info("⚠️  收到中断信号 (Ctrl+C)，将在当前epoch结束后退出...")
                self.logger.info("⚠️  正在保存模型和执行最终评估，请稍候...")
                self.logger.info("=" * 80)
                interrupted[0] = True
            else:
                self.logger.info("\n再次按Ctrl+C将强制退出（不保存）")
                raise KeyboardInterrupt
        
        original_handler = signal.signal(signal.SIGINT, signal_handler)

        best_epoch = 0
        best_val_loss = float('inf')
        counter = 0

        try:
            for epoch in range(self.start_epoch, self.epochs):
                # 检查是否收到中断信号
                if interrupted[0]:
                    self.logger.info(f"在epoch {epoch}处中断训练")
                    break
                    
                # Train
                train_loss_record = self.train(epoch)
                self.logger.info(f"Epoch {epoch+1}/{self.epochs} | Train Loss: {train_loss_record.loss_dict['train_loss'].avg:.2e} | LR: {self.optimizer.param_groups[0]['lr']:.6f}")

                if self.wandb:
                    import wandb
                    wandb.log({'epoch': epoch, **train_loss_record.to_dict()})

                if self.saving_ckpt and (epoch + 1) % self.ckpt_freq == 0:
                    ckpt_path = os.path.join(self.saving_path, f"checkpoint_{epoch}.pth")
                    torch.save({
                        'epoch': epoch+1,
                        'model_state_dict': self.model.state_dict(),
                        'optimizer_state_dict': self.optimizer.state_dict(),
                        'train_loss': train_loss_record.to_dict(),
                        'valid_metrics': None,
                    }, ckpt_path)
                    self.logger.info(f"Checkpoint saved: epoch {epoch}")

                if (epoch + 1) % self.eval_freq == 0:
                    valid_loss_record = self.evaluate(split="valid")

                    if self.wandb:
                        import wandb
                        wandb.log({'epoch': epoch, **valid_loss_record.to_dict()})

                    # Check for improvement
                    val_loss = valid_loss_record.to_dict()['valid_loss']
                    
                    # ReduceLROnPlateau需要在验证后调用，传入验证损失
                    if self.scheduler is not None and isinstance(self.scheduler, torch.optim.lr_scheduler.ReduceLROnPlateau):
                        self.scheduler.step(val_loss)
                    
                    if val_loss < best_val_loss:
                        improvement = (best_val_loss - val_loss) / best_val_loss * 100 if best_val_loss != float('inf') else 0
                        self.logger.info(f"New best model! Improvement: {improvement:.2f}%")
                        best_val_loss = val_loss
                        best_epoch = epoch
                        counter = 0

                        if self.saving_best:
                            best_model_path = os.path.join(self.saving_path, "best_model.pth")
                            torch.save({
                                'epoch': epoch,
                                'model_state_dict': self.model.state_dict(),
                                'optimizer_state_dict': self.optimizer.state_dict(),
                                'train_loss': train_loss_record.to_dict(),
                                'valid_metrics': valid_loss_record.to_dict(),
                            }, best_model_path)
                    else:
                        counter += 1
                        if self.patience != -1 and counter >= self.patience:
                            self.logger.info(f"Early stopping at epoch {epoch+1}")
                            break
        
        finally:
            # 恢复原始信号处理器
            signal.signal(signal.SIGINT, original_handler)

        # Final evaluation
        self.logger.info("=" * 80)
        if interrupted[0]:
            self.logger.info("⚠️  Training Interrupted by User!")
            self.logger.info(f"⚠️  Completed {epoch+1} epochs before interruption")
        else:
            self.logger.info("Training Completed!")
        self.logger.info("=" * 80)

        if self.saving_best and os.path.exists(os.path.join(self.saving_path, "best_model.pth")):
            checkpoint = torch.load(os.path.join(self.saving_path, "best_model.pth"))
            self.model.load_state_dict(checkpoint['model_state_dict'])
            self.logger.info(f"Loaded best model from epoch {best_epoch+1}")


        # Save final test metrics and sample predictions
        if self.saving_best:
            valid_loss_record = self.evaluate(split="valid", return_predictions=True, save_predictions=True)[0]
            test_loss_record = self.evaluate(split="test", return_predictions=True, save_predictions=True)[0]

            metrics_path = os.path.join(self.saving_path, "final_metrics.npz")
            np.savez(metrics_path,
                     valid_metrics=valid_loss_record.to_dict(),
                     test_metrics=test_loss_record.to_dict())
            self.logger.info(f"Saved final metrics to {metrics_path}")

            self._save_sample_train_predictions(sample_ratio=0.1)  # Save 10% of training data

            # Generate MD format training report
            self._generate_training_report(best_epoch, best_val_loss, test_loss_record)

        if self.wandb:
            import wandb
            wandb.run.summary["best_epoch"] = best_epoch
            wandb.run.summary.update(test_loss_record.to_dict())

        self.logger.info("=" * 80)

    def test(self, train_sample_ratio=0.1):
        """Test mode - save predictions for visualization (including train/valid/test)
        
        Args:
            train_sample_ratio: float, ratio of training samples to save (default: 0.1 = 10%)
        """
        self.logger.info("=" * 80)
        self.logger.info("Running Test Mode")
        self.logger.info("=" * 80)
        
        # Verify model is loaded
        if not hasattr(self, 'model') or self.model is None:
            raise ValueError("Model not loaded! Please provide --model_path")
        
        self.logger.info(f"Model loaded from: {self.args.get('model_path', 'N/A')}")
        self.logger.info(f"Saving results to: {self.saving_path}")

        # Evaluate on all splits and save predictions
        self.logger.info("\n" + "-" * 80)
        self.logger.info("Evaluating and saving predictions for all splits...")
        self.logger.info("-" * 80)
        
        # 1. Save validation predictions
        self.logger.info("\n[1/3] Evaluating validation set...")
        valid_loss_record = self.evaluate(split="valid", return_predictions=True, save_predictions=True)
        
        # 2. Save test predictions
        self.logger.info("\n[2/3] Evaluating test set...")
        test_loss_record = self.evaluate(split="test", return_predictions=True, save_predictions=True)
        
        # 3. Save sampled training predictions
        self.logger.info(f"\n[3/3] Sampling and saving {train_sample_ratio*100:.0f}% of training predictions...")
        self._save_sample_train_predictions(sample_ratio=train_sample_ratio)

        # Save all metrics
        metrics_path = os.path.join(self.saving_path, "test_metrics.npz")
        np.savez(metrics_path, 
                 valid_metrics=valid_loss_record[0].to_dict(),
                 test_metrics=test_loss_record[0].to_dict())
        self.logger.info(f"\nSaved all metrics to {metrics_path}")

        self.logger.info("\n" + "=" * 80)
        self.logger.info("✅ Test completed successfully!")
        self.logger.info("=" * 80)
        self.logger.info("\nSaved predictions:")
        self.logger.info(f"  - {self.saving_path}/train_predictions/  (sampled ~{train_sample_ratio*100:.0f}%)")
        self.logger.info(f"  - {self.saving_path}/valid_predictions/  (100%)")
        self.logger.info(f"  - {self.saving_path}/test_predictions/   (100%)")
        self.logger.info(f"\nMetrics saved to: {metrics_path}")
        self.logger.info("\nUse visualize.py for visualization.")
        self.logger.info("=" * 80)

        # Generate test report in MD format
        self._generate_test_report(valid_loss_record[0], test_loss_record[0])

    def _save_predictions(self, predictions_data, split):
        """Save predictions and ground truth for visualization

        Args:
            predictions_data: dict with keys 'inputs', 'predictions', 'targets', 'patch_indices'
        """
        self.logger.info("Saving predictions for visualization...")

        # Create predictions directory
        pred_dir = os.path.join(self.saving_path, f"{split}_predictions")
        os.makedirs(pred_dir, exist_ok=True)

        # Save metadata
        metadata = {
            'mask': self.mask if hasattr(self, 'mask') else None,
            'mask_per_region': self.dataset.mask_per_region if hasattr(self.dataset, 'mask_per_region') else None,
            'lat': self.lat if hasattr(self, 'lat') else None,
            'lon': self.lon if hasattr(self, 'lon') else None,
            'patches_per_day': self.dataset.patches_per_day if hasattr(self.dataset, 'patches_per_day') else None,
            'num_samples': len(predictions_data['predictions']),
            'normalization_mode': getattr(self.dataset, 'normalization_mode', None) if hasattr(self.dataset, 'normalization_mode') else None
        }

        # Save all data
        np.savez(os.path.join(pred_dir, "all_predictions.npz"), **predictions_data)
        np.savez(os.path.join(pred_dir, "metadata.npz"), **metadata)

        self.logger.info(f"Saved {len(predictions_data['predictions'])} samples to {pred_dir}")

    def _save_sample_train_predictions(self, sample_ratio=0.1):
        """Save a subset of training predictions for visualization
        
        Args:
            sample_ratio: float, ratio of training samples to save (default: 0.1 = 10%)
        """
        self.logger.info(f"Saving {sample_ratio*100:.0f}% of training predictions...")
        
        self.model.eval()
        
        # Containers for sampled predictions
        all_inputs = []
        all_predictions = []
        all_targets = []
        all_patch_indices = []
        
        # Calculate how many samples to save
        total_samples = len(self.train_loader.dataset)
        num_samples_to_save = int(total_samples * sample_ratio)
        samples_saved = 0
        
        # Calculate sampling interval
        sample_interval = max(1, int(1 / sample_ratio))
        
        with torch.no_grad():
            for batch_idx, batch_data in enumerate(tqdm(self.train_loader, desc="Sampling train predictions")):
                # Only process every Nth batch to get the desired ratio
                if batch_idx % sample_interval != 0:
                    continue
                
                if len(batch_data) == 3:
                    x, y, patch_idx = batch_data
                    patch_idx = patch_idx.numpy()
                else:
                    raise ValueError("Batch data must include patch_idx")
                
                x = x.to(self.device)
                y = y.to(self.device)
                
                # Get predictions
                _, y_pred_real = self.predict(x)
                
                # Denormalize targets
                if self.dataset is not None and hasattr(self.dataset, 'denormalize_data'):
                    y_real = self.dataset.denormalize_data(y)
                else:
                    y_real = y
                
                # Store data
                all_inputs.append(x.cpu().numpy())
                all_predictions.append(y_pred_real.cpu().numpy())
                all_targets.append(y_real.cpu().numpy())
                all_patch_indices.append(patch_idx)
                
                samples_saved += x.shape[0]
                
                # Stop when we have enough samples
                if samples_saved >= num_samples_to_save:
                    break
        
        if len(all_inputs) > 0:
            predictions_data = {
                'inputs': np.concatenate(all_inputs, axis=0),
                'predictions': np.concatenate(all_predictions, axis=0),
                'targets': np.concatenate(all_targets, axis=0),
                'patch_indices': np.concatenate(all_patch_indices, axis=0)
            }
            
            # Save using existing method
            self._save_predictions(predictions_data, 'train')
            self.logger.info(f"Saved {samples_saved}/{total_samples} training samples ({samples_saved/total_samples*100:.1f}%)")
        else:
            self.logger.warning("No training predictions were saved")

    def _generate_training_report(self, best_epoch, best_val_loss, test_loss_record):
        """Generate MD format training report using report_generator.py

        Args:
            best_epoch: int, best epoch number
            best_val_loss: float, best validation loss
            test_loss_record: LossRecord, test loss record
        """
        try:
            import json
            import time
            from pathlib import Path

            self.logger.info("=" * 80)
            self.logger.info("📝 Generating training report in MD format...")
            self.logger.info("=" * 80)

            # Prepare config data for report
            config_data = {
                'model': {
                    'name': self.args.get('model', {}).get('name', 'Unknown'),
                    'type': self.args.get('model', {}).get('type', 'Unknown'),
                    'path': self.args.get('model', {}).get('path', 'N/A'),
                    'num_params': self.args.get('model', {}).get('num_params', 'N/A'),
                    'embed_dim': self.args.get('model', {}).get('embed_dim', 'N/A'),
                    'window_size': self.args.get('model', {}).get('window_size', 'N/A'),
                    'patch_size': self.args.get('model', {}).get('patch_size', 'N/A'),
                },
                'data': {
                    'name': self.args.get('data', {}).get('name', 'Unknown'),
                    'timesteps': self.args.get('data', {}).get('timesteps', 'N/A'),
                    'shape': self.args.get('data', {}).get('shape', 'N/A'),
                    'in_channels': self.args.get('data', {}).get('in_channels', 'N/A'),
                    'input_len': self.args.get('data', {}).get('input_len', 'N/A'),
                    'output_len': self.args.get('data', {}).get('output_len', 'N/A'),
                    'train_ratio': self.args.get('data', {}).get('train_ratio', 0.8),
                    'valid_ratio': self.args.get('data', {}).get('valid_ratio', 0.1),
                    'test_ratio': self.args.get('data', {}).get('test_ratio', 0.1),
                    'train_samples': len(self.train_loader.dataset) if hasattr(self, 'train_loader') else 'N/A',
                    'test_samples': len(self.test_loader.dataset) if hasattr(self, 'test_loader') else 'N/A',
                },
                'train': {
                    'epochs': self.epochs,
                    'train_batchsize': self.args.get('train', {}).get('batchsize', 'N/A'),
                    'final_lr': self.optimizer.param_groups[0]['lr'] if self.optimizer else 'N/A',
                    'scheduler': type(self.scheduler).__name__ if self.scheduler else 'N/A',
                    'grad_clip': self.args.get('train', {}).get('grad_clip', 'N/A'),
                    'patience': self.patience,
                    'eval_freq': self.eval_freq,
                    'distribute_mode': self.args.get('train', {}).get('distribute_mode', '单GPU'),
                },
                'optimizer': {
                    'optimizer': type(self.optimizer).__name__ if self.optimizer else 'N/A',
                    'lr': self.args.get('optimizer', {}).get('lr', 'N/A'),
                    'weight_decay': self.args.get('optimizer', {}).get('weight_decay', 'N/A'),
                }
            }

            # Prepare metrics data for report
            test_metrics_dict = test_loss_record.to_dict()
            metrics_data = {
                'best_epoch': best_epoch + 1,
                'best_loss': best_val_loss,
                'best_rmse': test_metrics_dict.get('test_rmse', 0),
                'best_r2': test_metrics_dict.get('test_r2', 0),
                'best_mae': test_metrics_dict.get('test_mae', 0),
                'model_path': os.path.join(self.saving_path, "best_model.pth"),
                'total_time': time.time() - self.args.get('start_time', time.time()),
                'gpu_info': {
                    'name': torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU',
                    'memory': f"{torch.cuda.get_device_properties(0).total_memory / 1e9:.2f}" if torch.cuda.is_available() else 'N/A',
                    'mode': 'Single GPU' if torch.cuda.is_available() else 'CPU',
                    'cuda_version': torch.version.cuda if torch.cuda.is_available() else 'N/A',
                },
                'test_metrics': {
                    'r2': test_metrics_dict.get('test_r2', 0),
                    'rmse': test_metrics_dict.get('test_rmse', 0),
                    'mae': test_metrics_dict.get('test_mae', 0),
                    'mse': test_metrics_dict.get('test_mse', 0),
                    'mape': test_metrics_dict.get('test_mape', 0),
                },
                'valid_history': []  # Could be populated from training history if tracked
            }

            # Save config and metrics as JSON for report generator
            config_json_path = os.path.join(self.saving_path, "report_config.json")
            metrics_json_path = os.path.join(self.saving_path, "report_metrics.json")

            with open(config_json_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)

            with open(metrics_json_path, 'w', encoding='utf-8') as f:
                json.dump(metrics_data, f, indent=2, ensure_ascii=False)

            self.logger.info(f"✓ Saved report config to: {config_json_path}")
            self.logger.info(f"✓ Saved report metrics to: {metrics_json_path}")

            # Call report generator
            report_output_path = os.path.join(self.saving_path, "training_report.md")

            # Import and use report generator
            from pathlib import Path
            current_dir = Path(__file__).parent.parent
            import sys
            sys.path.insert(0, str(current_dir))

            from report_generator import PredictionReportGenerator

            generator = PredictionReportGenerator()
            report_path = generator.generate_train_report(
                config=config_data,
                metrics=metrics_data,
                output_path=report_output_path
            )

            self.logger.info("=" * 80)
            self.logger.info(f"✅ Training report generated: {report_path}")
            self.logger.info("=" * 80)

        except Exception as e:
            self.logger.error(f"⚠️  Failed to generate training report: {e}")
            self.logger.error("Training completed successfully, but report generation failed.")
            import traceback
            traceback.print_exc()

    def _generate_test_report(self, valid_loss_record, test_loss_record):
        """Generate MD format test report using report_generator.py

        Args:
            valid_loss_record: LossRecord, validation loss record
            test_loss_record: LossRecord, test loss record
        """
        try:
            import json
            import time
            from pathlib import Path

            self.logger.info("=" * 80)
            self.logger.info("📝 Generating test report in MD format...")
            self.logger.info("=" * 80)

            # Prepare config data (similar to training report)
            config_data = {
                'model': {
                    'name': self.args.get('model', {}).get('name', 'Unknown'),
                    'type': self.args.get('model', {}).get('type', 'Unknown'),
                    'path': self.args.get('model_path', 'N/A'),
                    'num_params': self.args.get('model', {}).get('num_params', 'N/A'),
                    'embed_dim': self.args.get('model', {}).get('embed_dim', 'N/A'),
                    'window_size': self.args.get('model', {}).get('window_size', 'N/A'),
                    'patch_size': self.args.get('model', {}).get('patch_size', 'N/A'),
                },
                'data': {
                    'name': self.args.get('data', {}).get('name', 'Unknown'),
                    'timesteps': self.args.get('data', {}).get('timesteps', 'N/A'),
                    'shape': self.args.get('data', {}).get('shape', 'N/A'),
                    'in_channels': self.args.get('data', {}).get('in_channels', 'N/A'),
                    'input_len': self.args.get('data', {}).get('input_len', 'N/A'),
                    'output_len': self.args.get('data', {}).get('output_len', 'N/A'),
                    'train_ratio': self.args.get('data', {}).get('train_ratio', 0.8),
                    'valid_ratio': self.args.get('data', {}).get('valid_ratio', 0.1),
                    'test_ratio': self.args.get('data', {}).get('test_ratio', 0.1),
                    'train_samples': len(self.train_loader.dataset) if hasattr(self, 'train_loader') else 'N/A',
                    'test_samples': len(self.test_loader.dataset) if hasattr(self, 'test_loader') else 'N/A',
                },
                'train': {
                    'epochs': 'N/A',
                    'train_batchsize': self.args.get('train', {}).get('batchsize', 'N/A'),
                    'distribute_mode': self.args.get('train', {}).get('distribute_mode', '单GPU'),
                },
                'optimizer': {
                    'optimizer': 'N/A',
                    'lr': 'N/A',
                    'weight_decay': 'N/A',
                }
            }

            # Prepare metrics data for report
            valid_metrics_dict = valid_loss_record.to_dict()
            test_metrics_dict = test_loss_record.to_dict()
            metrics_data = {
                'best_epoch': 'N/A',
                'best_loss': valid_metrics_dict.get('valid_loss', 0),
                'best_rmse': test_metrics_dict.get('test_rmse', 0),
                'best_r2': test_metrics_dict.get('test_r2', 0),
                'best_mae': test_metrics_dict.get('test_mae', 0),
                'model_path': self.args.get('model_path', 'N/A'),
                'total_time': 0,
                'gpu_info': {
                    'name': torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU',
                    'memory': f"{torch.cuda.get_device_properties(0).total_memory / 1e9:.2f}" if torch.cuda.is_available() else 'N/A',
                    'mode': 'Single GPU' if torch.cuda.is_available() else 'CPU',
                    'cuda_version': torch.version.cuda if torch.cuda.is_available() else 'N/A',
                },
                'test_metrics': {
                    'r2': test_metrics_dict.get('test_r2', 0),
                    'rmse': test_metrics_dict.get('test_rmse', 0),
                    'mae': test_metrics_dict.get('test_mae', 0),
                    'mse': test_metrics_dict.get('test_mse', 0),
                    'mape': test_metrics_dict.get('test_mape', 0),
                },
                'valid_history': []
            }

            # Save config and metrics as JSON
            config_json_path = os.path.join(self.saving_path, "test_report_config.json")
            metrics_json_path = os.path.join(self.saving_path, "test_report_metrics.json")

            with open(config_json_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)

            with open(metrics_json_path, 'w', encoding='utf-8') as f:
                json.dump(metrics_data, f, indent=2, ensure_ascii=False)

            self.logger.info(f"✓ Saved test report config to: {config_json_path}")
            self.logger.info(f"✓ Saved test report metrics to: {metrics_json_path}")

            # Call report generator
            report_output_path = os.path.join(self.saving_path, "test_report.md")

            # Import and use report generator
            from pathlib import Path
            current_dir = Path(__file__).parent.parent
            import sys
            sys.path.insert(0, str(current_dir))

            from report_generator import PredictionReportGenerator

            generator = PredictionReportGenerator()
            report_path = generator.generate_train_report(
                config=config_data,
                metrics=metrics_data,
                output_path=report_output_path
            )

            self.logger.info("=" * 80)
            self.logger.info(f"✅ Test report generated: {report_path}")
            self.logger.info("=" * 80)

        except Exception as e:
            self.logger.error(f"⚠️  Failed to generate test report: {e}")
            self.logger.error("Test completed successfully, but report generation failed.")
            import traceback
            traceback.print_exc()
