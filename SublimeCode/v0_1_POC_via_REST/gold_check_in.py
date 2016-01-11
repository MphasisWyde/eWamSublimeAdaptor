import sublime, sublime_plugin, ctypes, json, sys, http.client, socket
from . import gold_helpers, gold_environnement

class GoldCheckInCommand(sublime_plugin.TextCommand):

   def run(self, edit):
      gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
      # Callback "open_class" when name has been entered

      className = self.view.name().split('.')[0]
     
      conn = http.client.HTTPConnection('localhost:8082')
      conn.request("GET", "/aeWamManager/checkin/"+className)
      resp = conn.getresponse()

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
      
