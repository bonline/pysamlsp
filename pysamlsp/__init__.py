try:
    from pysamlsp import Pysamlsp
except ImportError:
    from pysamlsp import BasePysamlsp

__version_info__ = ('0', '1', '0')
__version__ = '.'.join(map(lambda x: str(x), __version_info__))
