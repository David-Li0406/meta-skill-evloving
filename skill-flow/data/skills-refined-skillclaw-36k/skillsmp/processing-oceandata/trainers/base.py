import os
import torch
import logging

try:
    import wandb
    WANDB_AVAILABLE = True
except ImportError:
    WANDB_AVAILABLE = False

import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

from tqdm import tqdm
from utils import LossRecord
from functools import partial
from models import _model_dict
from datasets import _dataset_dict


class BaseTrainer:
    def __init__(self, args):
        self.args = args
        self.model_args = args['model']
        self.data_args = args['data']
        self.optim_args = args['optimizer']
        self.scheduler_args = args['scheduler']
        self.train_args = args['train']
        self.log_args = args['log']

        if self.log_args.get('log', True):
            self.logger = logging.getLogger(__name__)
        else:
            class SimpleLogger:
                def info(self, msg): print(msg)
                def warning(self, msg): print(f"WARNING: {msg}")
                def error(self, msg): print(f"ERROR: {msg}")
            self.logger = SimpleLogger()

        self.wandb = self.log_args.get('wandb', False) and WANDB_AVAILABLE
        if self.wandb:
            wandb.init(
                project=self.log_args.get('wandb_project', 'default'),
                name=self.train_args.get('saving_name', 'experiment'),
                tags=[self.model_args.get('name', 'model'), self.data_args.get('name', 'dataset')],
                config=args)

        self.model_name = self.model_args['name']
        self.logger.info("Building {} model".format(self.model_name))
        self.model = self.build_model(**self.model_args)
        self.load_ckpt = self.train_args.get('load_ckpt', False)
        if self.load_ckpt:
            self.model.load_state_dict(torch.load(self.train_args['ckpt_path']))
            self.logger.info("Load model from {}".format(self.train_args['ckpt_path']))

        self._setup_gpu_configuration()

        self.optimizer = self.build_optimizer(**self.optim_args)
        self.scheduler = self.build_scheduler(**self.scheduler_args)
        self.criterion = torch.nn.MSELoss()

        self.logger.info("Model: {}".format(self.model))
        self.logger.info("Model parameters: {:.2f}M".format(sum(p.numel() for p in self.model.parameters()) / 1e6))

        self.data = self.data_args['dataset']
        self.logger.info("Loading {} dataset".format(self.data))
        self.train_loader, self.valid_loader, self.test_loader = self.build_data(**self.data_args)
        self.logger.info("Train dataset size: {}".format(len(self.train_loader.dataset)))
        self.logger.info("Valid dataset size: {}".format(len(self.valid_loader.dataset)))
        self.logger.info("Test dataset size: {}".format(len(self.test_loader.dataset)))

        self.epochs = self.train_args['epochs']
        self.eval_freq = self.train_args['eval_freq']
        self.patience = self.train_args['patience']

        self.saving_best = self.train_args.get('saving_best', True)
        self.saving_ckpt = self.train_args.get('saving_checkpoint', False)
        self.ckpt_freq = self.train_args.get('checkpoint_freq', 100)
        self.ckpt_max = self.train_args.get('checkpoint_max', 5)
        self.saving_path = self.train_args.get('saving_path', None)

    def _setup_gpu_configuration(self):
        self.device_ids = self.train_args.get('device_ids', [0])

        if isinstance(self.device_ids, int):
            self.device_ids = [self.device_ids]

        if not torch.cuda.is_available():
            self.logger.info("CUDA not available, using CPU")
            self.device = 'cpu'
            self.model = self.model.to(self.device)
            return

        # Validate device_ids before using them
        num_available_gpus = torch.cuda.device_count()
        for device_id in self.device_ids:
            if device_id >= num_available_gpus:
                raise ValueError(f"GPU {device_id} not available. Only {num_available_gpus} GPUs found.")

        num_requested_gpus = len(self.device_ids)
        self.distribute_mode = self.train_args.get('distribute_mode', 'DP')

        if num_requested_gpus > 1:
            if self.distribute_mode == 'DP':
                self.device = self.device_ids[0]  # Primary device for DataParallel
                self.model = self.model.to(self.device)
                self.model = torch.nn.DataParallel(self.model, device_ids=self.device_ids)
                self.logger.info(f"Using DataParallel with GPUs: {self.device_ids}")
            elif self.distribute_mode == 'DDP':
                self.device = self.device_ids[0]  # Primary device for DDP
                self.model = self.model.to(self.device)
                self._setup_ddp()
            else:
                self.logger.info(f"Unknown distribute_mode: {self.distribute_mode}, using single GPU")
                self.device = self.device_ids[0]
                self.model = self.model.to(self.device)
        else:
            # Single GPU mode
            self.device = self.device_ids[0]
            self.model = self.model.to(self.device)
            self.logger.info(f"Using single GPU: {self.device}")

    def _setup_ddp(self):
        """Setup DistributedDataParallel training"""
        try:
            if not dist.is_initialized():
                dist.init_process_group(backend='nccl')
            self.local_rank = self.train_args.get('local_rank', 0)
            torch.cuda.set_device(self.local_rank)
            self.model = self.model.to(self.local_rank)
            self.model = DDP(self.model, device_ids=[self.local_rank], output_device=self.local_rank)
            self.logger.info(f"Using DistributedDataParallel with local_rank: {self.local_rank}")
        except ImportError:
            self.logger.info("DDP not available, falling back to single GPU")
        except Exception as e:
            self.logger.info(f"DDP setup failed: {e}, falling back to single GPU")

    def get_initializer(self, name):
        if name is None:
            return None

        if name == 'xavier_normal':
            init_ = partial(torch.nn.init.xavier_normal_)
        elif name == 'kaiming_uniform':
            init_ = partial(torch.nn.init.kaiming_uniform_)
        elif name == 'kaiming_normal':
            init_ = partial(torch.nn.init.kaiming_normal_)
        return init_

    def build_optimizer(self, **kwargs):
        if self.optim_args['optimizer'] == 'Adam':
            optimizer = torch.optim.Adam(
                self.model.parameters(),
                lr=self.optim_args['lr'],
                weight_decay=self.optim_args['weight_decay'],
            )
        elif self.optim_args['optimizer'] == 'SGD':
            optimizer = torch.optim.SGD(
                self.model.parameters(),
                lr=self.optim_args['lr'],
                momentum=self.optim_args['momentum'],
                weight_decay=self.optim_args['weight_decay'],
            )
        elif self.optim_args['optimizer'] == 'AdamW':
            optimizer = torch.optim.AdamW(
                self.model.parameters(),
                lr=self.optim_args['lr'],
                weight_decay=self.optim_args['weight_decay'],
            )
        else:
            raise NotImplementedError("Optimizer {} not implemented".format(self.optim_args['optimizer']))
        return optimizer

    def build_scheduler(self, **kwargs):
        if self.scheduler_args['scheduler'] == 'MultiStepLR':
            scheduler = torch.optim.lr_scheduler.MultiStepLR(
                self.optimizer,
                milestones=self.scheduler_args['milestones'],
                gamma=self.scheduler_args['gamma'],
            )
        elif self.scheduler_args['scheduler'] == 'OneCycleLR':
            scheduler = torch.optim.lr_scheduler.OneCycleLR(
                self.optimizer,
                max_lr=self.optim_args['lr'],
                div_factor=self.scheduler_args['div_factor'],
                final_div_factor=self.scheduler_args['final_div_factor'],
                pct_start=self.scheduler_args['pct_start'],
                steps_per_epoch=self.scheduler_args['steps_per_epoch'],
                epochs=self.train_args['epochs'],
            )
        elif self.scheduler_args['scheduler'] == 'StepLR':
            scheduler = torch.optim.lr_scheduler.StepLR(
                self.optimizer,
                step_size=self.scheduler_args['step_size'],
                gamma=self.scheduler_args['gamma'],
            )
        elif self.scheduler_args['scheduler'] == 'CosineAnnealingWarmRestarts':
            scheduler = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(
                self.optimizer,
                T_0=self.scheduler_args['T_0'],
                T_mult=self.scheduler_args.get('T_mult', 1),
                eta_min=self.scheduler_args.get('eta_min', 0),
            )
        elif self.scheduler_args['scheduler'] == 'ReduceLROnPlateau':
            scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
                self.optimizer,
                mode=self.scheduler_args.get('mode', 'min'),
                factor=self.scheduler_args.get('factor', 0.5),
                patience=self.scheduler_args.get('patience', 10),
                min_lr=self.scheduler_args.get('min_lr', 0),
            )
        elif self.scheduler_args['scheduler'] == 'CosineAnnealingLR':
            scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
                self.optimizer,
                T_max=self.scheduler_args.get('T_max', self.train_args['epochs']),
                eta_min=self.scheduler_args.get('eta_min', 0),
            )
        else:
            scheduler = None
            if self.scheduler_args['scheduler'] is not None:
                raise NotImplementedError("Scheduler {} not implemented".format(self.scheduler_args['scheduler']))

        return scheduler

    def build_model(self, **kwargs):
        if self.model_name not in _model_dict:
            raise NotImplementedError("Model {} not implemented".format(self.model_name))
        model = _model_dict[self.model_name](self.model_args)
        return model

    def build_data(self, **kwargs):
        if self.data_args['name'].lower() not in _dataset_dict:
            raise NotImplementedError("Dataset {} not implemented".format(self.data_args['name']))
        # Pass mode to dataset if available
        mode = self.args.get('mode', 'train')
        dataset = _dataset_dict[self.data_args['name'].lower()](self.data_args, mode=mode)
        return dataset.train_loader, dataset.valid_loader, dataset.test_loader

    def process(self, **kwargs):
        self.logger.info("Start training")

        best_epoch = 0
        best_metrics = None
        counter = 0
        with tqdm(total=self.epochs) as bar:
            for epoch in range(self.epochs):
                train_loss_record = self.train(self.model, self.train_loader, self.optimizer, self.criterion, self.scheduler)
                self.logger.info("Epoch {} | {} | lr: {:.4f}".format(epoch, train_loss_record, self.optimizer.param_groups[0]["lr"]))
                if self.wandb:
                    wandb.log(train_loss_record.to_dict())

                if self.saving_ckpt and (epoch + 1) % self.ckpt_freq == 0:
                    torch.save({
                        'epoch': epoch,
                        'model_state_dict': self.model.cpu().state_dict(),
                        'optimizer_state_dict': self.optimizer.state_dict(),
                        'scheduler_state_dict': self.scheduler.state_dict(),
                        'train_loss_record': train_loss_record.to_dict(),
                        }, os.path.join(self.saving_path, "checkpoint_{}.pth".format(epoch)))
                    self.model.to(self.device)
                    self.logger.info("Epoch {} | Checkpoint saved".format(epoch))

                if (epoch + 1) % self.eval_freq == 0:
                    valid_loss_record = self.evaluate(self.model, self.valid_loader, self.criterion, split="valid")
                    self.logger.info("Epoch {} | {}".format(epoch, valid_loss_record))
                    valid_metrics = valid_loss_record.to_dict()

                    if self.wandb:
                        wandb.log(valid_loss_record.to_dict())

                    if not best_metrics or valid_metrics['valid_loss'] < best_metrics['valid_loss']:
                        counter = 0
                        best_epoch = epoch
                        best_metrics = valid_metrics
                        torch.save(self.model.cpu().state_dict(), os.path.join(self.saving_path, "best_model.pth"))
                        self.model.to(self.device)
                        self.logger.info("Epoch {} | Best model saved".format(epoch))
                    elif self.patience != -1:
                        counter += 1
                        if counter >= self.patience:
                            self.logger.info("Early stop at epoch {}".format(epoch))
                            break
                bar.update(1)

        self.logger.info("Optimization Finished!")

        if not best_metrics:
            torch.save(self.model.cpu().state_dict(), os.path.join(self.saving_path, "best_model.pth"))
        else:
            self.model.load_state_dict(torch.load(os.path.join(self.saving_path, "best_model.pth")))
            self.logger.info("Load best model at epoch {}".format(best_epoch))
        self.model.to(self.device)

        valid_loss_record = self.evaluate(self.model, self.valid_loader, self.criterion, split="valid")
        self.logger.info("Valid metrics: {}".format(valid_loss_record))
        test_loss_record = self.evaluate(self.model, self.test_loader, self.criterion, split="test")
        self.logger.info("Test metrics: {}".format(test_loss_record))

        if self.wandb:
            wandb.run.summary["best_epoch"] = best_epoch
            wandb.run.summary.update(test_loss_record.to_dict())
        try:
            from report_generator import PredictionReportGenerator

            # 准备配置数据
            config_data = {
                'model_type': self.model.__class__.__name__,
                'epochs': self.epochs,
                'batch_size': self.train_loader.batch_size,
                'learning_rate': self.optimizer.param_groups[0]['lr'],
                'optimizer': self.optimizer.__class__.__name__,
                'criterion': self.criterion.__class__.__name__,
            }

             # 准备指标数据
            metrics_data = {
               'best_epoch': best_epoch,
               'best_valid_loss': best_metrics['valid_loss'] if best_metrics else None,
               'final_valid_loss': valid_loss_record.to_dict()['valid_loss'],
               'final_test_loss': test_loss_record.to_dict()['test_loss'],
            }

            # 生成报告
            generator = PredictionReportGenerator()
            report_path = generator.generate_train_report(
               config=config_data,
               metrics=metrics_data,
               output_path=os.path.join(self.saving_path, 'training_report.md')
            )
            self.logger.info("Training report generated: {}".format(report_path))

        except Exception as e:
            self.logger.error("Failed to generate training report: {}".format(e))

            
    

    def train(self, model, train_loader, optimizer, criterion, scheduler=None, **kwargs):
        loss_record = LossRecord(["train_loss"])
        model.to(self.device)
        model.train()
        for x, y in train_loader:
            x = x.to(self.device)
            y = y.to(self.device)
            y_pred = model(x).reshape(y.shape)
            data_loss = criterion(y_pred, y)
            loss = data_loss
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            loss_record.update({"train_loss": loss.sum().item()}, n=y_pred.shape[0])

        if scheduler is not None:
            scheduler.step()
        return loss_record

    def evaluate(self, model, eval_loader, criterion, split="valid", **kwargs):
        loss_record = LossRecord(["{}_loss".format(split)])
        model.eval()
        with torch.no_grad():
            for x, y in eval_loader:
                x = x.to(self.device)
                y = y.to(self.device)
                y_pred = model(x).reshape(y.shape)
                data_loss = criterion(y_pred, y)
                loss = data_loss
                loss_record.update({"{}_loss".format(split): loss.sum().item()}, n=y_pred.shape[0])
        return loss_record
