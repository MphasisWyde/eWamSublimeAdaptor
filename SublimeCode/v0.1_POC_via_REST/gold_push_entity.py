import sublime, sublime_plugin, ctypes, json, User.gold_environnement, sys, http.client

class GoldPushEntityCommand(sublime_plugin.TextCommand):

   def run(self, edit):
      User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
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

      User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)

   def is_enabled(self):
      return User.gold_helpers.IsGoldCode(self.view)



      