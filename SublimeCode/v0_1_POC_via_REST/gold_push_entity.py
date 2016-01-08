import sublime, sublime_plugin, ctypes, json, sys, http.client
from . import *

class GoldPushEntityCommand(sublime_plugin.TextCommand):

   def run(self, edit):
      gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
      # Callback "open_class" when name has been entered

      className = self.view.name().split('.')[0]
      print(className)
      source = self.view.substr(sublime.Region(0, self.view.size())).translate(str.maketrans( {'"': '\\\"' } ))
      print(source)
      
      conn = http.client.HTTPConnection('localhost:8082')
      conn.request("POST", "/aeWamManager/aModuleDef/"+className, source)
      resp = conn.getresponse()
      print(resp.status)
      print(resp.read())

      gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)

   def is_enabled(self):
      try:
         className = self.view.name().split('.')[0]
         conn = http.client.HTTPConnection('localhost', 8082, timeout=0.1)
         conn.request("GET", "/aeWamManager/entitystatus/"+className)
         resp = conn.getresponse()
         parsed = json.loads(resp.read().decode("ascii").replace('\r\n', '\n'))

         return gold_helpers.IsGoldCode(self.view) and parsed['checkedOut']
      except socket.timeout:
         sublime.status_message("*** WARNING: EWAM SERVICE UNREACHABLE ! ***")
         return False


      