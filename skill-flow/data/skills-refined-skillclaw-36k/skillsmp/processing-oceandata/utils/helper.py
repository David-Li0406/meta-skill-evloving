import numpy as np
import torch
import yaml
import logging
import os
import pytz
import shutil
from datetime import datetime
from datetime import datetime


def set_seed(seed):
    np.random.seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    torch.manual_seed(seed)


def set_device(cuda, device):
    if cuda is True and torch.cuda.is_available():
        torch.cuda.set_device(device=device)


def load_config(args):
    with open(args['config'], 'r') as stream:
        config = yaml.load(stream, yaml.FullLoader)

    model_name = config['model']['name']
    model_mapping_path = 'configs/models/model_mapping.yaml'

    try:
        with open(model_mapping_path, 'r') as f:
            model_mapping = yaml.load(f, yaml.FullLoader)

        if model_name in model_mapping:
            model_config_path = model_mapping[model_name]
            with open(model_config_path, 'r') as f:
                model_config = yaml.load(f, yaml.FullLoader)
            config['model'].update(model_config)
        else:
            logging.warning(f"Model {model_name} not found in model_mapping.yaml, using default config")
    except FileNotFoundError:
        logging.warning(f"Model mapping file not found at {model_mapping_path}")

    if 'mode' in args:
        config['mode'] = args['mode']
    if 'model_path' in args:
        config['model_path'] = args['model_path']

    return config


def save_config(args, saving_path):
    with open(os.path.join(saving_path, 'config.yaml'), 'w') as f:
        yaml.dump(args, f)


def get_dir_path(model, dataset, path):
    date = datetime.now().strftime("%m_%d")
    shanghai_tz = pytz.timezone('Asia/Shanghai')
    time = datetime.now(shanghai_tz).strftime("_%H_%M_%S")
    dir_path = os.path.join(path, dataset, date, model + time)
    os.makedirs(dir_path, exist_ok=True)
    dir_name = date + "_" + model + time
    return dir_path, dir_name


def set_up_logger(args):
    model = args['model']['name']
    dataset = args['data']['dataset']
    log_dir = args['log']['log_dir']

    local_rank = args.get('local_rank', 0)
    mode = args.get('mode', 'train')
    model_path = args.get('model_path', None)

    # Test mode requires model_path
    if mode == 'test':
        if model_path is None:
            raise ValueError("Test mode requires --model_path to be specified (path to model file)")
        if not os.path.exists(model_path):
            raise ValueError(f"Model file does not exist: {model_path}")
        # Extract directory from model file path
        log_dir = os.path.dirname(model_path)
        dir_name = os.path.basename(log_dir)
        logging.info(f"Test mode: using model directory: {log_dir}")
    else:
        # Train mode: always create new path with timestamp
        log_dir, dir_name = get_dir_path(model, dataset, log_dir)

    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        filename=os.path.join(log_dir, f"train_rank_{local_rank}.log")
    )

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)
    logging.info("Saving logs in: {}".format(log_dir))

    return log_dir, dir_name


def save_code(module, saving_path, with_dir=False, with_path=False):
    os.makedirs(os.path.join(saving_path, 'code'), exist_ok=True)

    if with_path:
        src = module
    else:
        if with_dir:
            src = os.path.dirname(module.__file__)
        else:
            src = module.__file__
    print('Saving code from {} to {}'.format(src, saving_path))
    dst = os.path.join(saving_path, 'code', os.path.basename(src))

    if os.path.isdir(src):
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)
