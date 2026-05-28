"""
Lightweight shim for sensai utilities used by solidlsp
"""
import pickle
import logging
from time import perf_counter


# Pickle utilities
def getstate(obj):
    """Get state for pickling"""
    return obj.__dict__ if hasattr(obj, '__dict__') else obj


def load_pickle(path):
    """Load pickle from file"""
    with open(path, 'rb') as f:
        return pickle.load(f)


def dump_pickle(obj, path):
    """Dump pickle to file"""
    with open(path, 'wb') as f:
        pickle.dump(obj, f)


# String utilities
class ToStringMixin:
    """Mixin for __str__ implementation"""
    
    def __str__(self):
        attrs = []
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                attrs.append(f"{key}={value}")
        return f"{self.__class__.__name__}({', '.join(attrs)})"


# Logging utilities
class LogTime:
    """Context manager for timing operations"""
    
    def __init__(self, name, logger=None):
        self.name = name
        self.logger = logger or logging.getLogger(__name__)
        self.start_time = None
    
    def __enter__(self):
        self.start_time = perf_counter()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = perf_counter() - self.start_time
        self.logger.debug(f"{self.name} took {elapsed:.2f}s")
        return False
