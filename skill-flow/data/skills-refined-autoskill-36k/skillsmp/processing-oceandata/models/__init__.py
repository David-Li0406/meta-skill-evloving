from .base import BaseModel
from .cnn_model import OceanCNN
from .resnet_model import OceanResNet
from .transformer_model import OceanTransformer
from .pangu import OceanPangu2, OceanPangu2Autoregressive
from .fengwu import OceanFengwu, OceanFengwuAutoregressive
from .fuxi import Fuxi, FuxiAutoregressive
from .nng import NNG, NNGAutoregressive
from .oneforcast import OneForecast, OneForecastAutoregressive
from .graphcast import GraphCast, GraphCastAutoregressive
from .crossformer import OceanCrossformer, OceanCrossformerAutoregressive


_model_dict = {
    "BaseModel": BaseModel,
    "OceanCNN": OceanCNN,
    "OceanResNet": OceanResNet,
    "OceanTransformer": OceanTransformer,

    # Fuxi model variants
    "Fuxi": Fuxi,
    "Fuxi_Light": Fuxi,  # Same class, different config
    "Fuxi_Full": Fuxi,   # Same class, different config
    "Fuxi_Auto": FuxiAutoregressive,  # Autoregressive version

    # NNG model variants
    "NNG": NNG,
    "NNG_Light": NNG,  # Same class, different config
    "NNG_Full": NNG,   # Same class, different config
    "NNG_Auto": NNGAutoregressive,  # Autoregressive vers

    # OneForecast model variants
    "OneForecast": OneForecast,
    "OneForecast_Light": OneForecast,      # Same class, different config
    "OneForecast_Balanced": OneForecast,   # Same class, different config  
    "OneForecast_Full": OneForecast,       # Same class, different config (original architecture)
    "OneForecast_Auto": OneForecastAutoregressive,  # Autoregressive version

    # GraphCast model variants
    "GraphCast": GraphCast,
    "GraphCast_Light": GraphCast,  # Same class, different config
    "GraphCast_Full": GraphCast,   # Same class, different config (original architecture)
    "GraphCast_Auto": GraphCastAutoregressive,  # Autoregressive version

    # Fengwu model variants (unified naming)
    "Fengwu": OceanFengwu,
    "Fengwu_Light": OceanFengwu,  # Same class, different config
    "Fengwu_Full": OceanFengwu,   # Same class, different config (original architecture)
    "Fengwu_Auto": OceanFengwuAutoregressive,  # Autoregressive version

    # Pangu model variants (unified naming) - Using Pangu2 as standard
    "Pangu": OceanPangu2,
    "Pangu_Light": OceanPangu2,  # Same class, different config
    "Pangu_Full": OceanPangu2,   # Same class, different config (original architecture)
    "Pangu_Auto": OceanPangu2Autoregressive,  # Autoregressive version

    # Crossformer model variants (spatiotemporal attention)
    "Crossformer": OceanCrossformer,
    "Crossformer_Light": OceanCrossformer,  # Same class, different config
    "Crossformer_Balanced": OceanCrossformer,  # Same class, different config (recommended)
    "Crossformer_Full": OceanCrossformer,   # Same class, different config (maximum capacity)
    "Crossformer_Auto": OceanCrossformerAutoregressive,  # Autoregressive version
}
