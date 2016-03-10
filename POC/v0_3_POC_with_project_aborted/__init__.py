import sublime, sys
from . import plugin_helpers


plugin_helpers.DebugLogMessage("--> " + __name__ + ": " + sys._getframe().f_code.co_name)

plugin_helpers.DebugLogMessage("<-- " + __name__ + ": " + sys._getframe().f_code.co_name)
