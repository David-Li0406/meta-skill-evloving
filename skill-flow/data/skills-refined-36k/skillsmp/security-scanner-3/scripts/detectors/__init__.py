"""检测器模块包"""

from .dangerous_calls import DangerousCallsDetector
from .network_ops import NetworkOpsDetector
from .file_ops import FileOpsDetector
from .obfuscation import ObfuscationDetector
from .data_exfil import DataExfilDetector

__all__ = [
    'DangerousCallsDetector',
    'NetworkOpsDetector',
    'FileOpsDetector',
    'ObfuscationDetector',
    'DataExfilDetector',
]
