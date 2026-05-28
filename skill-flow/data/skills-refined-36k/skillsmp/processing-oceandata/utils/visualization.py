"""
Ocean prediction visualization utilities

This module provides tools for visualizing ocean velocity predictions,
including loading data from test_predictions directory and creating
various plots (comparisons, velocity fields, temporal sequences, etc.)
"""

import matplotlib.pyplot as plt
import numpy as np
import logging
from pathlib import Path
from typing import Dict, Optional, Tuple, Union
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import TwoSlopeNorm

logger = logging.getLogger(__name__)


class OceanVisualizer:
    """
    Visualization utilities for ocean velocity predictions

    This class handles:
    1. Loading prediction data from test_predictions directory
    2. Creating various visualizations (velocity fields, comparisons, sequences)
    3. Applying masks and coordinate transformations
    """

    def __init__(self, predictions_dir: str):
        """
        Initialize visualizer with predictions directory

        Args:
            predictions_dir: Path to predictions directory containing:
                - all_predictions.npz: Model predictions and targets
                - metadata.npz: Coordinate and mask information

        The predictions_dir should be:
            logs/pearl_river/10_16/OceanCNN_13_22_08/test_predictions/
        """
        self.predictions_dir = Path(predictions_dir)

        # Validate directory exists
        if not self.predictions_dir.exists():
            raise FileNotFoundError(f"Predictions directory not found: {self.predictions_dir}")

        # Load data
        self.predictions_data = None
        self.metadata = None
        self._load_data()

        logger.info(f"Initialized OceanVisualizer with {self.num_samples} samples")

    def _load_data(self):
        """
        Load prediction data and metadata from npz files

        Data shapes after loading:
            predictions_data:
                - 'inputs': (N, T_in, C, H, W) - Input sequences
                - 'predictions': (N, T_out, C, H, W) - Model predictions
                - 'targets': (N, T_out, C, H, W) - Ground truth
                - 'patch_indices': (N,) - Region indices

            metadata:
                - 'lat': (H, W) - Latitude grid
                - 'lon': (H, W) - Longitude grid
                - 'mask': (H, W) - Global land mask (True=land, False=ocean)
                - 'mask_per_region': (num_regions, H, W) - Per-region masks
                - 'patches_per_day': int - Number of patches per day
                - 'num_samples': int - Total samples
        """
        # Load predictions
        pred_file = self.predictions_dir / "all_predictions.npz"
        if not pred_file.exists():
            raise FileNotFoundError(f"Predictions file not found: {pred_file}")

        self.predictions_data = dict(np.load(pred_file))
        logger.info(f"Loaded predictions from {pred_file}")
        logger.info(f"  - inputs shape: {self.predictions_data['inputs'].shape}")
        logger.info(f"  - predictions shape: {self.predictions_data['predictions'].shape}")
        logger.info(f"  - targets shape: {self.predictions_data['targets'].shape}")

        # Load metadata
        meta_file = self.predictions_dir / "metadata.npz"
        if meta_file.exists():
            self.metadata = dict(np.load(meta_file, allow_pickle=True))
            logger.info(f"Loaded metadata from {meta_file}")
            if 'lat' in self.metadata and self.metadata['lat'] is not None:
                logger.info(f"  - lat shape: {self.metadata['lat'].shape}")
                logger.info(f"  - lon shape: {self.metadata['lon'].shape}")
            if 'mask' in self.metadata and self.metadata['mask'] is not None:
                logger.info(f"  - mask shape: {self.metadata['mask'].shape}")
        else:
            logger.warning(f"Metadata file not found: {meta_file}")
            self.metadata = {}

    @property
    def num_samples(self) -> int:
        """Get total number of samples"""
        if self.predictions_data is None:
            return 0
        return len(self.predictions_data['predictions'])

    @property
    def lat(self) -> Optional[np.ndarray]:
        """Get latitude grid (H, W)"""
        if self.metadata and 'lat' in self.metadata:
            lat = self.metadata['lat']
            # Handle shape: (1, H, W) -> (H, W)
            if lat is not None and lat.ndim == 3 and lat.shape[0] == 1:
                lat = lat[0]
            return lat
        return None

    @property
    def lon(self) -> Optional[np.ndarray]:
        """Get longitude grid (H, W)"""
        if self.metadata and 'lon' in self.metadata:
            lon = self.metadata['lon']
            # Handle shape: (1, H, W) -> (H, W)
            if lon is not None and lon.ndim == 3 and lon.shape[0] == 1:
                lon = lon[0]
            return lon
        return None

    @property
    def mask(self) -> Optional[np.ndarray]:
        """Get land mask (H, W) - True for land, False for ocean"""
        if self.metadata and 'mask' in self.metadata:
            mask = self.metadata['mask']
            # Handle shape: (1, H, W) -> (H, W)
            if mask is not None and mask.ndim == 3 and mask.shape[0] == 1:
                mask = mask[0]
            return mask
        return None

    def get_sample(self, idx: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Get a specific sample by index

        Args:
            idx: Sample index (0 to num_samples-1)

        Returns:
            Tuple of (input, prediction, target):
                - input: (T_in, C, H, W) - Input sequence
                - prediction: (T_out, C, H, W) - Model prediction
                - target: (T_out, C, H, W) - Ground truth
        """
        if idx < 0 or idx >= self.num_samples:
            raise IndexError(f"Sample index {idx} out of range [0, {self.num_samples})")

        return (
            self.predictions_data['inputs'][idx],
            self.predictions_data['predictions'][idx],
            self.predictions_data['targets'][idx]
        )

    def _compute_velocity_magnitude(self, data: np.ndarray) -> np.ndarray:
        """
        Compute velocity magnitude from u, v components

        Args:
            data: Velocity data, shape (..., C, H, W) where C >= 2
                  data[..., 0, :, :] = u component
                  data[..., 1, :, :] = v component

        Returns:
            magnitude: (..., H, W) - Velocity magnitude sqrt(u^2 + v^2)
        """
        if data.shape[-3] < 2:
            # Only one channel, return as-is
            return data[..., 0, :, :]

        u = data[..., 0, :, :]  # (..., H, W)
        v = data[..., 1, :, :]  # (..., H, W)
        magnitude = np.sqrt(u**2 + v**2)  # (..., H, W)

        return magnitude

    def _apply_mask(self, data: np.ndarray, mask: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Apply land mask to data

        Args:
            data: Data array (..., H, W)
            mask: (H, W) boolean mask (True=land, False=ocean)
                  If None, uses self.mask

        Returns:
            Masked array with land pixels masked out
        """
        if mask is None:
            mask = self.mask

        if mask is not None:
            return np.ma.masked_where(mask, data)
        return data

    def plot_velocity_field(
        self,
        data: np.ndarray,
        title: str = "Ocean Velocity",
        save_path: Optional[str] = None,
        use_cartopy: bool = False,
        mask: Optional[np.ndarray] = None
    ):
        """
        Plot a single velocity field

        Args:
            data: Velocity data, one of:
                  - (C, H, W): Single frame
                  - (T, C, H, W): Temporal sequence (will use first frame)
            title: Plot title
            save_path: Path to save figure
            use_cartopy: Use cartopy for geographic projection
            mask: Optional mask to apply (uses self.mask if None)

        Shape transformations:
            Input: (C, H, W) or (T, C, H, W)
            -> Extract first time step if needed: (C, H, W)
            -> Compute magnitude: u=(H,W), v=(H,W) -> mag=(H,W)
            -> Apply mask: (H,W) -> masked_array(H,W)
            -> Plot on (lon, lat) grid
        """
        # Handle temporal dimension
        if data.ndim == 4:  # (T, C, H, W)
            data = data[0]  # Take first time step -> (C, H, W)

        # Compute magnitude
        magnitude = self._compute_velocity_magnitude(data)  # (H, W)
        magnitude = self._apply_mask(magnitude, mask)

        # Extract u, v for quiver plot
        if data.shape[0] >= 2:
            u = self._apply_mask(data[0], mask)  # (H, W)
            v = self._apply_mask(data[1], mask)  # (H, W)
            has_vectors = True
        else:
            has_vectors = False

        # Create figure
        if use_cartopy and self.lat is not None and self.lon is not None:
            fig = plt.figure(figsize=(15, 8))
            ax = plt.axes(projection=ccrs.PlateCarree())

            # Plot magnitude
            im = ax.pcolormesh(
                self.lon, self.lat, magnitude,
                transform=ccrs.PlateCarree(),
                cmap='viridis', shading='auto'
            )

            # Plot velocity vectors
            if has_vectors:
                skip = max(1, min(self.lat.shape) // 30)
                ax.quiver(
                    self.lon[::skip, ::skip], self.lat[::skip, ::skip],
                    u[::skip, ::skip], v[::skip, ::skip],
                    transform=ccrs.PlateCarree(),
                    scale=5, width=0.002, color='white', alpha=0.7
                )

            # Add features
            ax.add_feature(cfeature.LAND, facecolor='lightgray')
            ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
            ax.gridlines(draw_labels=True, linewidth=0.5, alpha=0.5)

            plt.colorbar(im, ax=ax, label='Velocity Magnitude (m/s)', shrink=0.6)
        else:
            fig, ax = plt.subplots(figsize=(12, 8))

            # Use lat/lon if available, otherwise use pixel coordinates
            if self.lat is not None and self.lon is not None:
                x, y = self.lon, self.lat
                xlabel, ylabel = 'Longitude', 'Latitude'
            else:
                x, y = np.arange(magnitude.shape[1]), np.arange(magnitude.shape[0])
                xlabel, ylabel = 'X', 'Y'

            # Plot magnitude
            im = ax.pcolormesh(x, y, magnitude, cmap='viridis', shading='auto')

            # Plot vectors
            if has_vectors:
                skip = max(1, min(magnitude.shape) // 30)
                ax.quiver(
                    x[::skip, ::skip], y[::skip, ::skip],
                    u[::skip, ::skip], v[::skip, ::skip],
                    scale=5, width=0.002, color='white', alpha=0.7
                )

            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            plt.colorbar(im, ax=ax, label='Velocity Magnitude (m/s)')

        ax.set_title(title)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            logger.info(f"Saved velocity field to {save_path}")

        return fig

    def plot_comparison(
        self,
        sample_idx: int,
        time_step: int = 0,
        save_path: Optional[str] = None,
        use_cartopy: bool = False
    ):
        """
        Plot ground truth vs prediction comparison for a sample

        Args:
            sample_idx: Sample index to visualize
            time_step: Time step to visualize (for multi-step predictions)
            save_path: Path to save figure
            use_cartopy: Use cartopy for geographic projection

        Shape transformations:
            1. Get sample: prediction=(T_out, C, H, W), target=(T_out, C, H, W)
            2. Extract time step: prediction=(C, H, W), target=(C, H, W)
            3. Compute magnitude: (C, H, W) -> (H, W)
            4. Compute error: |pred - target| -> (H, W)
            5. Apply mask: (H, W) -> masked_array(H, W)
            6. Plot on (lon, lat) grid
        """
        # Get data
        _, prediction, target = self.get_sample(sample_idx)
        # prediction: (T_out, C, H, W)
        # target: (T_out, C, H, W)

        # Extract time step
        pred_t = prediction[time_step]  # (C, H, W)
        target_t = target[time_step]    # (C, H, W)

        # Compute magnitudes
        pred_mag = self._compute_velocity_magnitude(pred_t)    # (H, W)
        target_mag = self._compute_velocity_magnitude(target_t)  # (H, W)
        error = np.abs(pred_mag - target_mag)  # (H, W)

        # Apply mask
        pred_mag = self._apply_mask(pred_mag)
        target_mag = self._apply_mask(target_mag)
        error = self._apply_mask(error)

        # Create figure
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))

        # Determine coordinate system
        if self.lat is not None and self.lon is not None:
            x, y = self.lon, self.lat
            xlabel, ylabel = 'Longitude', 'Latitude'
        else:
            x = np.arange(pred_mag.shape[1])
            y = np.arange(pred_mag.shape[0])
            xlabel, ylabel = 'X', 'Y'

        # Ground truth
        im1 = axes[0].pcolormesh(x, y, target_mag, cmap='viridis', shading='auto')
        axes[0].set_title('Ground Truth')
        axes[0].set_xlabel(xlabel)
        axes[0].set_ylabel(ylabel)
        plt.colorbar(im1, ax=axes[0], label='Velocity (m/s)')

        # Prediction
        im2 = axes[1].pcolormesh(x, y, pred_mag, cmap='viridis', shading='auto')
        axes[1].set_title('Prediction')
        axes[1].set_xlabel(xlabel)
        axes[1].set_ylabel(ylabel)
        plt.colorbar(im2, ax=axes[1], label='Velocity (m/s)')

        # Error
        im3 = axes[2].pcolormesh(x, y, error, cmap='Reds', shading='auto')
        axes[2].set_title('Absolute Error')
        axes[2].set_xlabel(xlabel)
        axes[2].set_ylabel(ylabel)
        plt.colorbar(im3, ax=axes[2], label='Error (m/s)')

        plt.suptitle(f'Sample {sample_idx}, Time Step {time_step}', fontsize=14)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            logger.info(f"Saved comparison to {save_path}")

        return fig

    def plot_temporal_sequence(
        self,
        sample_idx: int,
        data_type: str = 'prediction',
        save_path: Optional[str] = None,
        max_frames: int = 8
    ):
        """
        Plot temporal sequence (input, prediction, or target)

        Args:
            sample_idx: Sample index
            data_type: 'input', 'prediction', or 'target'
            save_path: Path to save figure
            max_frames: Maximum number of frames to display

        Shape transformations:
            1. Get data: (T, C, H, W)
            2. For each time step t:
               - Extract frame: (C, H, W)
               - Compute magnitude: (H, W)
               - Apply mask: masked_array(H, W)
            3. Plot grid of time steps
        """
        # Get data
        input_seq, pred_seq, target_seq = self.get_sample(sample_idx)

        # Select sequence based on data_type
        if data_type == 'input':
            sequence = input_seq  # (T_in, C, H, W)
            title = f'Sample {sample_idx}: Input Sequence'
        elif data_type == 'prediction':
            sequence = pred_seq   # (T_out, C, H, W)
            title = f'Sample {sample_idx}: Prediction Sequence'
        elif data_type == 'target':
            sequence = target_seq # (T_out, C, H, W)
            title = f'Sample {sample_idx}: Target Sequence'
        else:
            raise ValueError(f"Invalid data_type: {data_type}")

        # Limit number of frames
        T = min(sequence.shape[0], max_frames)

        # Determine grid layout
        cols = min(4, T)
        rows = (T + cols - 1) // cols

        fig, axes = plt.subplots(rows, cols, figsize=(4*cols, 3*rows))
        if rows == 1 and cols == 1:
            axes = np.array([[axes]])
        elif rows == 1:
            axes = axes.reshape(1, -1)
        elif cols == 1:
            axes = axes.reshape(-1, 1)

        # Plot each time step
        for t in range(T):
            row = t // cols
            col = t % cols
            ax = axes[row, col]

            # Extract frame and compute magnitude
            frame = sequence[t]  # (C, H, W)
            magnitude = self._compute_velocity_magnitude(frame)  # (H, W)
            magnitude = self._apply_mask(magnitude)

            # Plot
            if self.lat is not None and self.lon is not None:
                im = ax.pcolormesh(self.lon, self.lat, magnitude, cmap='viridis', shading='auto')
                ax.set_xlabel('Lon')
                ax.set_ylabel('Lat')
            else:
                im = ax.imshow(magnitude, cmap='viridis', origin='lower')
                ax.set_xlabel('X')
                ax.set_ylabel('Y')

            ax.set_title(f'T={t}')
            plt.colorbar(im, ax=ax, label='m/s')

        # Hide empty subplots
        for t in range(T, rows * cols):
            row = t // cols
            col = t % cols
            axes[row, col].axis('off')

        plt.suptitle(title, fontsize=14)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            logger.info(f"Saved temporal sequence to {save_path}")

        return fig

    def plot_statistics(self, save_path: Optional[str] = None):
        """
        Plot overall statistics across all samples

        Creates a 2x2 grid showing:
        1. Error distribution histogram
        2. Prediction vs target scatter plot
        3. Per-sample mean error
        4. Mean spatial error heatmap

        Shape transformations:
            predictions: (N, T_out, C, H, W)
            targets: (N, T_out, C, H, W)
            -> Flatten for histogram/scatter: (N*T_out*C*H*W,)
            -> Mean over space for per-sample: (N,)
            -> Mean over samples/time for heatmap: (H, W)
        """
        predictions = self.predictions_data['predictions']  # (N, T_out, C, H, W)
        targets = self.predictions_data['targets']          # (N, T_out, C, H, W)

        # Compute errors
        errors = np.abs(predictions - targets)  # (N, T_out, C, H, W)

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))

        # 1. Error distribution
        axes[0, 0].hist(errors.flatten(), bins=50, alpha=0.7, color='blue', edgecolor='black')
        axes[0, 0].set_xlabel('Absolute Error')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].set_title('Error Distribution')
        axes[0, 0].grid(True, alpha=0.3)

        # 2. Prediction vs Target scatter
        pred_flat = predictions.flatten()
        target_flat = targets.flatten()
        # Subsample for performance
        subsample = min(10000, len(pred_flat))
        indices = np.random.choice(len(pred_flat), subsample, replace=False)
        axes[0, 1].scatter(target_flat[indices], pred_flat[indices], alpha=0.3, s=1)
        axes[0, 1].plot([target_flat.min(), target_flat.max()],
                        [target_flat.min(), target_flat.max()], 'r--', lw=2, label='Perfect')
        axes[0, 1].set_xlabel('Ground Truth')
        axes[0, 1].set_ylabel('Prediction')
        axes[0, 1].set_title('Prediction vs Ground Truth')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)

        # 3. Per-sample mean error
        # Mean over (T_out, C, H, W) -> (N,)
        sample_errors = np.mean(errors, axis=(1, 2, 3, 4))
        axes[1, 0].plot(sample_errors, marker='o', markersize=2, linewidth=0.5)
        axes[1, 0].set_xlabel('Sample Index')
        axes[1, 0].set_ylabel('Mean Absolute Error')
        axes[1, 0].set_title('Error per Sample')
        axes[1, 0].grid(True, alpha=0.3)

        # 4. Spatial error heatmap
        # Mean over (N, T_out, C) -> (H, W)
        spatial_error = np.mean(errors, axis=(0, 1, 2))
        spatial_error = self._apply_mask(spatial_error)

        if self.lat is not None and self.lon is not None:
            im = axes[1, 1].pcolormesh(self.lon, self.lat, spatial_error, cmap='Reds', shading='auto')
            axes[1, 1].set_xlabel('Longitude')
            axes[1, 1].set_ylabel('Latitude')
        else:
            im = axes[1, 1].imshow(spatial_error, cmap='Reds', origin='lower')
            axes[1, 1].set_xlabel('X')
            axes[1, 1].set_ylabel('Y')

        axes[1, 1].set_title('Mean Spatial Error')
        plt.colorbar(im, ax=axes[1, 1], label='MAE')

        plt.suptitle('Prediction Statistics', fontsize=16, fontweight='bold')
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            logger.info(f"Saved statistics to {save_path}")

        return fig

    def close_all(self):
        """Close all matplotlib figures"""
        plt.close('all')

