"""
MAT Data Visualization Script

This script visualizes ocean data from MAT files with three types of plots:
1. Spatial visualization: u and v velocity fields
2. Data distribution histograms: u, v, and adt (if available)
3. Time series visualization: u and v at specific locations
"""

import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.gridspec import GridSpec
import os
import argparse
from pathlib import Path
import glob


def find_project_root(start_path=None):
    """
    Find project root directory by looking for .claude or .git directories

    Args:
        start_path: Starting path for search (default: current directory)

    Returns:
        Path to project root directory
    """
    if start_path is None:
        start_path = Path.cwd()
    else:
        start_path = Path(start_path)

    current = start_path.resolve()

    # Search upward for .claude or .git directory
    while current != current.parent:
        if (current / '.claude').exists() or (current / '.git').exists():
            return current
        current = current.parent

    # If not found, return the starting path
    print(f"Warning: Could not find project root (.claude or .git), using current directory")
    return start_path


def find_mat_files(search_dir):
    """
    Find all .mat files in the specified directory and its subdirectories

    Args:
        search_dir: Directory to search for .mat files

    Returns:
        List of paths to .mat files
    """
    mat_files = []

    # Search in the root directory
    mat_files.extend(glob.glob(str(search_dir / '*.mat')))

    # Search in common data directories
    data_dirs = ['data', 'datasets', 'Data', 'Datasets']
    for data_dir in data_dirs:
        data_path = search_dir / data_dir
        if data_path.exists():
            mat_files.extend(glob.glob(str(data_path / '*.mat')))
            mat_files.extend(glob.glob(str(data_path / '**' / '*.mat'), recursive=True))

    return sorted(set(mat_files))  # Remove duplicates and sort


def load_mat_data(mat_path):
    """
    Load data from MAT file

    Args:
        mat_path: Path to the .mat file

    Returns:
        data_dict: Dictionary containing u, v, x, y, and optionally adt
    """
    print(f"Loading MAT file from {mat_path}")
    mat_data = scipy.io.loadmat(mat_path)

    # Extract data
    data_dict = {}

    # Required fields
    if 'u_combined' in mat_data:
        data_dict['u'] = mat_data['u_combined']  # (time, H, W)
        print(f"  u shape: {data_dict['u'].shape}")
    else:
        raise ValueError("MAT file must contain 'u_combined' field")

    if 'v_combined' in mat_data:
        data_dict['v'] = mat_data['v_combined']  # (time, H, W)
        print(f"  v shape: {data_dict['v'].shape}")
    else:
        raise ValueError("MAT file must contain 'v_combined' field")

    # Optional coordinate grids
    if 'x' in mat_data:
        data_dict['lon'] = mat_data['x']  # (H, W) or (1, H, W)
        print(f"  lon shape: {data_dict['lon'].shape}")

    if 'y' in mat_data:
        data_dict['lat'] = mat_data['y']  # (H, W) or (1, H, W)
        print(f"  lat shape: {data_dict['lat'].shape}")

    # Optional adt field
    if 'adt_combined' in mat_data or 'adt' in mat_data:
        adt_key = 'adt_combined' if 'adt_combined' in mat_data else 'adt'
        data_dict['adt'] = mat_data[adt_key]  # (time, H, W)
        print(f"  adt shape: {data_dict['adt'].shape}")
    else:
        print("  adt not found in MAT file")

    # Generate mask from NaN values
    mask_u = np.isnan(data_dict['u'])
    mask_v = np.isnan(data_dict['v'])
    data_dict['mask'] = mask_u | mask_v  # (time, H, W)

    return data_dict


def plot_spatial_visualization(data_dict, time_idx=0, save_dir='./'):
    """
    Plot spatial visualization of u and v velocity fields

    Args:
        data_dict: Dictionary containing u, v, lat, lon, mask
        time_idx: Time index to visualize (default: 0)
        save_dir: Directory to save plots
    """
    print(f"\n=== Generating Spatial Visualization (time_idx={time_idx}) ===")

    u = data_dict['u'][time_idx]  # (H, W)
    v = data_dict['v'][time_idx]  # (H, W)
    mask = data_dict['mask'][time_idx]  # (H, W)

    # Get coordinates if available
    if 'lon' in data_dict and 'lat' in data_dict:
        lon = data_dict['lon']
        lat = data_dict['lat']

        # Handle different shapes
        if lon.ndim == 3:
            lon = lon[0]
            lat = lat[0]

        use_coords = True
        xlabel = 'Longitude'
        ylabel = 'Latitude'
    else:
        # Use grid indices
        H, W = u.shape
        lon, lat = np.meshgrid(np.arange(W), np.arange(H))
        use_coords = False
        xlabel = 'Grid X'
        ylabel = 'Grid Y'

    # Mask NaN values
    u_masked = np.ma.masked_where(mask, u)
    v_masked = np.ma.masked_where(mask, v)

    # Create figure with two subplots
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.patch.set_facecolor('white')

    # Plot u velocity
    axes[0].set_facecolor('lightgray')
    im1 = axes[0].pcolormesh(lon, lat, u_masked, cmap='seismic', shading='auto')
    axes[0].set_title(f'U Velocity (Eastward) - Time Index {time_idx}', fontsize=14, fontweight='bold')
    axes[0].set_xlabel(xlabel, fontsize=12)
    axes[0].set_ylabel(ylabel, fontsize=12)
    axes[0].set_aspect('equal', adjustable='box')
    plt.colorbar(im1, ax=axes[0], label='U velocity (m/s)')

    # Plot v velocity
    axes[1].set_facecolor('lightgray')
    im2 = axes[1].pcolormesh(lon, lat, v_masked, cmap='seismic', shading='auto')
    axes[1].set_title(f'V Velocity (Northward) - Time Index {time_idx}', fontsize=14, fontweight='bold')
    axes[1].set_xlabel(xlabel, fontsize=12)
    axes[1].set_ylabel(ylabel, fontsize=12)
    axes[1].set_aspect('equal', adjustable='box')
    plt.colorbar(im2, ax=axes[1], label='V velocity (m/s)')

    plt.tight_layout()

    save_path = os.path.join(save_dir, f'spatial_visualization_t{time_idx}.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved spatial visualization to {save_path}")
    plt.close()


def plot_data_distribution(data_dict, save_dir='./'):
    """
    Plot data distribution histograms for u, v, and adt (if available)

    Args:
        data_dict: Dictionary containing u, v, and optionally adt
        save_dir: Directory to save plots
    """
    print(f"\n=== Generating Data Distribution Histograms ===")

    # Prepare data
    variables = []
    labels = []
    colors_list = []

    # U velocity
    u_valid = data_dict['u'][~data_dict['mask']]
    variables.append(u_valid)
    labels.append('U velocity (m/s)')
    colors_list.append('steelblue')

    # V velocity
    v_valid = data_dict['v'][~data_dict['mask']]
    variables.append(v_valid)
    labels.append('V velocity (m/s)')
    colors_list.append('coral')

    # ADT (if available)
    if 'adt' in data_dict:
        adt = data_dict['adt']
        # Use the same mask or generate from adt
        if adt.shape == data_dict['mask'].shape:
            adt_mask = data_dict['mask'] | np.isnan(adt)
        else:
            adt_mask = np.isnan(adt)

        adt_valid = adt[~adt_mask]
        variables.append(adt_valid)
        labels.append('ADT (m)')
        colors_list.append('seagreen')

    # Create figure
    n_vars = len(variables)
    fig, axes = plt.subplots(1, n_vars, figsize=(6*n_vars, 5))

    if n_vars == 1:
        axes = [axes]

    # Plot histograms
    for i, (var, label, color) in enumerate(zip(variables, labels, colors_list)):
        axes[i].hist(var.flatten(), bins=100, color=color, alpha=0.7, edgecolor='black')
        axes[i].set_xlabel(label, fontsize=12)
        axes[i].set_ylabel('Frequency', fontsize=12)
        axes[i].set_title(f'{label.split("(")[0].strip()} Distribution', fontsize=14, fontweight='bold')
        axes[i].grid(True, alpha=0.3)

        # Add statistics
        mean_val = np.mean(var)
        std_val = np.std(var)
        median_val = np.median(var)

        stats_text = f'Mean: {mean_val:.4f}\nStd: {std_val:.4f}\nMedian: {median_val:.4f}'
        axes[i].text(0.02, 0.98, stats_text, transform=axes[i].transAxes,
                    verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
                    fontsize=10)

    plt.tight_layout()

    save_path = os.path.join(save_dir, 'data_distribution_histograms.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved distribution histograms to {save_path}")
    plt.close()


def plot_time_series(data_dict, location=None, save_dir='./'):
    """
    Plot time series of u and v velocities at a specific location

    Args:
        data_dict: Dictionary containing u, v, mask
        location: (i, j) tuple for spatial location, if None will select center of valid region
        save_dir: Directory to save plots
    """
    print(f"\n=== Generating Time Series Visualization ===")

    u = data_dict['u']  # (time, H, W)
    v = data_dict['v']  # (time, H, W)
    mask = data_dict['mask']  # (time, H, W)

    time_steps = u.shape[0]

    # Auto-select location if not provided
    if location is None:
        # Find a valid ocean location (not masked at any timestep)
        valid_mask = ~np.any(mask, axis=0)  # (H, W) - True where always valid

        if np.any(valid_mask):
            # Find center of valid region
            valid_indices = np.argwhere(valid_mask)
            center_idx = len(valid_indices) // 2
            location = tuple(valid_indices[center_idx])
            print(f"Auto-selected location: {location}")
        else:
            # Use first location that has some valid data
            valid_at_t0 = ~mask[0]
            if np.any(valid_at_t0):
                valid_indices = np.argwhere(valid_at_t0)
                location = tuple(valid_indices[0])
                print(f"Selected first valid location: {location}")
            else:
                raise ValueError("No valid ocean locations found in data")

    i, j = location
    print(f"Plotting time series at location ({i}, {j})")

    # Extract time series
    u_series = u[:, i, j]
    v_series = v[:, i, j]

    # Create time axis
    time_axis = np.arange(time_steps)

    # Create figure with single plot showing both U and V
    fig, ax = plt.subplots(1, 1, figsize=(14, 6))

    # Plot both u and v velocity on the same plot
    ax.plot(time_axis, u_series, color='steelblue', linewidth=1.5, label='U velocity (Eastward)', alpha=0.8)
    ax.plot(time_axis, v_series, color='coral', linewidth=1.5, label='V velocity (Northward)', alpha=0.8)

    ax.set_xlabel('Time Index', fontsize=12)
    ax.set_ylabel('Velocity (m/s)', fontsize=12)
    ax.set_title(f'Velocity Time Series at Location ({i}, {j})', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right', fontsize=11)

    # Add statistics box
    u_mean = np.nanmean(u_series)
    u_std = np.nanstd(u_series)
    v_mean = np.nanmean(v_series)
    v_std = np.nanstd(v_series)

    stats_text = (f'U: Mean={u_mean:.4f} m/s, Std={u_std:.4f} m/s\n'
                  f'V: Mean={v_mean:.4f} m/s, Std={v_std:.4f} m/s')
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
            fontsize=10)

    plt.tight_layout()

    save_path = os.path.join(save_dir, f'time_series_loc_{i}_{j}.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved time series to {save_path}")
    plt.close()


def main():
    """Main function to generate all visualizations"""
    parser = argparse.ArgumentParser(description='Visualize MAT ocean data')
    parser.add_argument('--mat_path', type=str, default=None,
                       help='Path to MAT file (if not provided, will auto-detect)')
    parser.add_argument('--save_dir', type=str, default=None,
                       help='Directory to save plots (default: <project_root>/outputs/plots)')
    parser.add_argument('--time_idx', type=int, default=0,
                       help='Time index for spatial visualization (default: 0)')
    parser.add_argument('--location', type=str, default=None,
                       help='Location for time series as "i,j" (e.g., "50,50"), if None will auto-select')

    args = parser.parse_args()

    # Find project root
    project_root = find_project_root()
    print(f"Project root: {project_root}")

    # Auto-detect MAT file if not provided
    if args.mat_path is None:
        print("\nSearching for MAT files...")
        mat_files = find_mat_files(project_root)

        if not mat_files:
            raise FileNotFoundError(
                f"No MAT files found in {project_root}\n"
                f"Please specify --mat_path explicitly or place a .mat file in the project root"
            )

        if len(mat_files) == 1:
            args.mat_path = mat_files[0]
            print(f"Found 1 MAT file: {args.mat_path}")
        else:
            print(f"Found {len(mat_files)} MAT files:")
            for i, mat_file in enumerate(mat_files):
                print(f"  [{i}] {mat_file}")

            # Use the first one by default
            args.mat_path = mat_files[0]
            print(f"\nUsing: {args.mat_path}")
            print(f"To use a different file, specify --mat_path explicitly")
    else:
        args.mat_path = str(Path(args.mat_path).resolve())
        print(f"Using specified MAT file: {args.mat_path}")

    # Set default save directory if not provided
    if args.save_dir is None:
        args.save_dir = project_root / 'outputs' / 'plots'
    else:
        args.save_dir = Path(args.save_dir)

    # Create save directory
    args.save_dir = Path(args.save_dir)
    args.save_dir.mkdir(parents=True, exist_ok=True)
    print(f"Saving plots to: {args.save_dir}")

    # Load data
    data_dict = load_mat_data(args.mat_path)

    # Parse location if provided
    location = None
    if args.location is not None:
        try:
            location = tuple(map(int, args.location.split(',')))
            print(f"Using specified location: {location}")
        except:
            print(f"Invalid location format '{args.location}', will auto-select")

    # Generate visualizations
    print("\n" + "="*60)

    # 1. Spatial visualization
    plot_spatial_visualization(data_dict, time_idx=args.time_idx, save_dir=str(args.save_dir))

    # 2. Data distribution histograms
    plot_data_distribution(data_dict, save_dir=str(args.save_dir))

    # 3. Time series visualization
    plot_time_series(data_dict, location=location, save_dir=str(args.save_dir))

    print("\n" + "="*60)
    print("All visualizations completed successfully!")
    print(f"Plots saved to: {args.save_dir}")
    print(f"\nGenerated files:")
    for plot_file in sorted(args.save_dir.glob('*.png')):
        print(f"  - {plot_file.name}")


if __name__ == '__main__':
    main()
