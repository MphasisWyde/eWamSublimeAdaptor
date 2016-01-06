import sublime, sublime_plugin, ctypes, json, User.gold_environnement, sys, http.client

class GoldOpenClassCommand(sublime_plugin.TextCommand):

   def run(self, edit):
      User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
      # Callback "open_class" when name has been entered
      sublime.active_window().show_input_panel("Enter class name:", "", self.open_class, None, None)

'''
   def is_enabled(self):
      if not User.gold_environnement.IsEnvironnementInitialized():
         if User.gold_helpers.IsGoldProjectLoaded():
            User.gold_environnement.InitializeEnvironnement(User.gold_environnement.GetPath())

      return User.gold_environnement.IsEnvironnementInitialized()
'''

   # Forward call to another command that will actually create a new view. We are forced to do this because at the time this callback is called, the run function has ended, and the "edit" object isn't valid  anymore. Problem is that we need it to insert text in the new view.
   def open_class(self, className):
     self.view.run_command("gold_do_open_class", {"className": className})


class GoldDoOpenClassCommand(sublime_plugin.TextCommand):

   def run(self, edit, className):

      '''
      request = b"""
      {
         "eWamRequest":
         {
            "myId":0,
            "myPid":0,
            "myUser":"Developer",
            "myVersion":"00.00",
            "myRequest":"getSource",
            "myParams":
            {
               "classId":0,
               "classNsid":0,
               "classVersion":0,
               "className":\"""" + className.encode('ascii') + b"""\",
               "classSrc":"",
               "ancestor":"aApplicativeRoot"
            }
         }
      }"""

      result = ctypes.c_char_p( User.gold_environnement.hWamAPI.execEwamCmd(0, request) )
      print(result.value.decode('ascii'))
      jsonObj = json.loads(result.value.decode('ascii'))
      '''

      conn = http.client.HTTPConnection('localhost:8082')

      conn.request("GET", "/aeWamManager/aModuleDef/"+className)
      resp = conn.getresponse()
      newView = sublime.active_window().new_file()

      #newView.set_scratch(True)
      newView.set_name(className + ".gold")
      newView.insert(edit, 0, jsonObj['eWamReply']['myResult'].replace('\r\n', '\n'))

      newView.insert(edit, 0, resp.read().decode("ascii").replace('\r\n', '\n'))
      #newView.insert(edit, 0, jsonObj['eWamReply']['myResult'])

      # Probably rather use 'Packages/Gold/gold.tmLanguage' : consider the user has installed the plugin package 'Gold'
      newView.set_syntax_file('Packages/User/gold.tmLanguage')

      print(resp.status, resp.reason, resp.read())
      conn.close()

      User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)