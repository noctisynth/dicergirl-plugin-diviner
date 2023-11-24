from .handlers import commands
from .utils import init


init()

__version__ = "2.0.0"

__type__ = "plugin"
__name__ = "diviner"
__nbhandler__ = handlers
__nbcommands__ = commands
__description__ = "基于古蓍草占卜算法."