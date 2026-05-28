import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

# Enable detailed crash reporting
import faulthandler
faulthandler.enable()

import argparse
from utils import set_up_logger, set_seed, load_config, get_dir_path, save_config
from procedures.base import base_procedure
from procedures.ocean_procedure import ocean_procedure
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


def main():
    parser = argparse.ArgumentParser(description='Neural Framework for Ocean Prediction')
    parser.add_argument("--mode", type=str, choices=["train", "test"], default="train",
                       help="Training mode: train or test")
    parser.add_argument("--config", type=str, default="./configs/pearl_river_config.yaml",
                       help="Path to configuration file")
    parser.add_argument("--model_path", type=str, default=None,
                       help="Path to existing model directory (for test mode or continue training)")

    args = parser.parse_args()
    args = vars(args)

    args = load_config(args)

    saving_path, saving_name = set_up_logger(args)

    args['train']['saving_path'] = saving_path # complete path to save the model
    args['train']['saving_name'] = saving_name # save floder name
    save_config(args, saving_path)
    set_seed(args['train']['random_seed'])

    dataset_name = args['data']['name']
    if dataset_name == 'Base':
        base_procedure(args)
    elif dataset_name in ['ocean', 'surface', 'mid', 'pearl_river']:
        ocean_procedure(args)
    else:
        raise NotImplementedError(f"Dataset {dataset_name} not implemented")


if __name__ == "__main__":
    main()
