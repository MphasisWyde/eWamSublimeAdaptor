import sublime, sublime_plugin, sys, http.client, socket
from . import *

class GoldTestCommand(sublime_plugin.ApplicationCommand):

    def run(self):
        gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)

        gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)

    def is_enabled(self):
        try:
            conn = http.client.HTTPConnection('localhost', 8082, timeout=0.3)
            conn.request("GET", "/aeWamManager/aModuleDef/aTest")
            resp = conn.getresponse()

            return True
        except socket.timeout:
            sublime.status_message("*** WARNING: EWAM SERVICE UNREACHABLE ! ***")
            return False