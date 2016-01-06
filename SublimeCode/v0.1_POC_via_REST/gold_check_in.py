import sublime, sublime_plugin, ctypes, json, User.gold_environnement, sys, http.client

class GoldCheckInCommand(sublime_plugin.TextCommand):

   def run(self, edit):
      User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
      # Callback "open_class" when name has been entered

      className = self.view.name().split('.')[0]
     
      conn = http.client.HTTPConnection('localhost:8082')
      conn.request("GET", "/aeWamManager/checkin/"+className)
      resp = conn.getresponse()

      User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)

   def is_enabled(self):
      return User.gold_helpers.IsGoldCode(self.view)