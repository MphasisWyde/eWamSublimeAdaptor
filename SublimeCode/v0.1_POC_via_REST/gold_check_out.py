import sublime, sublime_plugin, ctypes, json, User.gold_environnement, sys, http.client

class GoldCheckOutCommand(sublime_plugin.TextCommand):

   def run(self, edit):
      User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
      # Callback "open_class" when name has been entered

      className = self.view.name().split('.')[0]
     
      conn = http.client.HTTPConnection('localhost:8082')
      conn.request("GET", "/aeWamManager/checkout/"+className)
      resp = conn.getresponse()

      User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)

   def is_enabled(self):
      className = self.view.name().split('.')[0]
      conn = http.client.HTTPConnection('localhost',8082, 1)
      conn.request("GET", "/aeWamManager/entitystatus/"+className)
      resp = conn.getresponse()
      parsed = json.loads(resp.read().decode("ascii").replace('\r\n', '\n'))
      print('check out: ',parsed['checkedOut'])

      return User.gold_helpers.IsGoldCode(self.view) and not parsed['checkedOut']