import logging
from trainers.ocean_trainer import OceanTrainer


def ocean_procedure(args):
    """Procedure for ocean velocity prediction"""
    logger = logging.getLogger(__name__)

    # data_info save in the same path
    if 'saving_path' in args['train']:
        args['data']['saving_path'] = args['train']['saving_path']

    trainer = OceanTrainer(args)

    mode = args.get('mode', 'train')

    if mode == 'train':
        trainer.process()
    elif mode == 'test':
        trainer.test()
    else:
        raise ValueError(f"Unknown mode: {mode}")

    logger.info("Ocean prediction procedure completed")
