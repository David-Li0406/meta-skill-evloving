from .base import MyDataset
from .ocean_dataset import OceanDataset

_dataset_dict = {
    'mydataset': MyDataset,
    'ocean': OceanDataset,          # 海洋数据集类（通用）
    'surface': OceanDataset,        # 表层海洋数据 (patches_per_day=147)
    'mid': OceanDataset,            # 中层海洋数据 (patches_per_day=131)
    'pearl_river': OceanDataset,    # 珠江口数据 (patches_per_day=1, MAT format)
}
