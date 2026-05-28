#!/usr/bin/env python3
"""
Visualization script for ocean prediction results

This script loads prediction data from test_predictions directory and
creates various visualizations including comparisons, temporal sequences,
and statistical plots.

Usage:
    python visualize.py --pred_dir logs/pearl_river/10_16/OceanCNN_13_22_08/test_predictions
    python visualize.py --pred_dir logs/pearl_river/10_16/OceanCNN_13_22_08/test_predictions --sample_idx 0 --num_samples 5
    python visualize.py --pred_dir logs/pearl_river/10_16/OceanCNN_13_22_08/test_predictions --output_dir visualizations
"""

import argparse
import logging
from pathlib import Path
from utils import OceanVisualizer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description='Visualize ocean prediction results',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Visualize first 5 samples
  python visualize.py --pred_dir logs/pearl_river/10_16/OceanCNN_13_22_08/test_predictions --num_samples 5

  # Visualize specific sample
  python visualize.py --pred_dir logs/pearl_river/10_16/OceanCNN_13_22_08/test_predictions --sample_idx 10

  # Visualize with custom output directory
  python visualize.py --pred_dir logs/pearl_river/10_16/OceanCNN_13_22_08/test_predictions --output_dir my_visualizations

  # Visualize input/prediction/target sequences
  python visualize.py --pred_dir logs/pearl_river/10_16/OceanCNN_13_22_08/test_predictions --sample_idx 0 --show_sequences

  # Generate only statistics plot
  python visualize.py --pred_dir logs/pearl_river/10_16/OceanCNN_13_22_08/test_predictions --stats_only
        """
    )

    # Required arguments
    parser.add_argument(
        '--pred_dir',
        type=str,
        required=True,
        help='Path to predictions directory (must contain all_predictions.npz and metadata.npz)'
    )

    # Sample selection
    parser.add_argument(
        '--sample_idx',
        type=int,
        default=None,
        help='Specific sample index to visualize (0 to num_samples-1). If not specified, visualizes first num_samples'
    )
    parser.add_argument(
        '--num_samples',
        type=int,
        default=5,
        help='Number of samples to visualize (default: 5). Only used if sample_idx is not specified'
    )

    # Visualization options
    parser.add_argument(
        '--time_step',
        type=int,
        default=0,
        help='Time step to visualize for multi-step predictions (default: 0)'
    )
    parser.add_argument(
        '--show_sequences',
        action='store_true',
        help='Also plot temporal sequences (input, prediction, target)'
    )
    parser.add_argument(
        '--use_cartopy',
        action='store_true',
        help='Use cartopy for geographic projections (requires cartopy installed)'
    )
    parser.add_argument(
        '--stats_only',
        action='store_true',
        help='Generate only statistics plot, skip individual samples'
    )

    # Output options
    parser.add_argument(
        '--output_dir',
        type=str,
        default=None,
        help='Output directory for visualizations (default: pred_dir/visualizations)'
    )
    parser.add_argument(
        '--dpi',
        type=int,
        default=150,
        help='DPI for saved figures (default: 150)'
    )

    args = parser.parse_args()

    # Create output directory
    if args.output_dir is None:
        output_dir = Path(args.pred_dir) / 'visualizations'
    else:
        output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info("=" * 80)
    logger.info("Ocean Prediction Visualization")
    logger.info("=" * 80)
    logger.info(f"Predictions directory: {args.pred_dir}")
    logger.info(f"Output directory: {output_dir}")

    # Initialize visualizer
    try:
        visualizer = OceanVisualizer(args.pred_dir)
    except Exception as e:
        logger.error(f"Failed to initialize visualizer: {e}")
        return

    logger.info(f"Loaded {visualizer.num_samples} samples")
    logger.info("=" * 80)

    # Generate statistics plot
    if args.stats_only or (args.sample_idx is None and args.num_samples > 0):
        logger.info("Generating statistics plot...")
        try:
            visualizer.plot_statistics(save_path=str(output_dir / "statistics.png"))
            logger.info("✓ Statistics plot saved")
        except Exception as e:
            logger.error(f"Failed to generate statistics: {e}")

    # Skip individual samples if stats_only
    if args.stats_only:
        logger.info("=" * 80)
        logger.info("Visualization completed!")
        logger.info(f"Results saved to: {output_dir}")
        return

    # Determine samples to visualize
    if args.sample_idx is not None:
        # Visualize specific sample
        sample_indices = [args.sample_idx]
    else:
        # Visualize first num_samples
        sample_indices = list(range(min(args.num_samples, visualizer.num_samples)))

    # Visualize each sample
    for idx in sample_indices:
        logger.info(f"Processing sample {idx}...")

        try:
            # 1. Comparison plot (Ground Truth vs Prediction vs Error)
            logger.info(f"  - Creating comparison plot...")
            visualizer.plot_comparison(
                sample_idx=idx,
                time_step=args.time_step,
                save_path=str(output_dir / f"comparison_sample_{idx:03d}_t{args.time_step}.png"),
                use_cartopy=args.use_cartopy
            )

            # 2. Temporal sequences (optional)
            if args.show_sequences:
                logger.info(f"  - Creating temporal sequences...")

                # Input sequence
                try:
                    visualizer.plot_temporal_sequence(
                        sample_idx=idx,
                        data_type='input',
                        save_path=str(output_dir / f"input_sequence_sample_{idx:03d}.png")
                    )
                except Exception as e:
                    logger.warning(f"  - Failed to plot input sequence: {e}")

                # Prediction sequence
                try:
                    visualizer.plot_temporal_sequence(
                        sample_idx=idx,
                        data_type='prediction',
                        save_path=str(output_dir / f"prediction_sequence_sample_{idx:03d}.png")
                    )
                except Exception as e:
                    logger.warning(f"  - Failed to plot prediction sequence: {e}")

                # Target sequence
                try:
                    visualizer.plot_temporal_sequence(
                        sample_idx=idx,
                        data_type='target',
                        save_path=str(output_dir / f"target_sequence_sample_{idx:03d}.png")
                    )
                except Exception as e:
                    logger.warning(f"  - Failed to plot target sequence: {e}")

            logger.info(f"✓ Sample {idx} completed")

        except Exception as e:
            logger.error(f"✗ Failed to process sample {idx}: {e}")
            continue

    # Clean up
    visualizer.close_all()

    logger.info("=" * 80)
    logger.info("Visualization completed!")
    logger.info(f"Results saved to: {output_dir}")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()

