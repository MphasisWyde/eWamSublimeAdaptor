import sublime, sublime_plugin, ctypes, json, sys
from . import gold_environnement, gold_helpers

class GoldSaveClassCommand(sublime_plugin.TextCommand):

   def run(self, edit):
      gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
      # Callback "open_class" when name has been entered
      sublime.active_window().show_input_panel("Enter class name:", "", self.open_class, None, None)

   def is_enabled(self):
      if not gold_environnement.IsEnvironnementInitialized():
         if gold_helpers.IsGoldProjectLoaded():
            gold_environnement.InitializeEnvironnement(gold_environnement.GetPath())
      return gold_environnement.IsEnvironnementInitialized()

   # Forward call to another command that will actually create a new view. We are forced to do this because at the time this callback is called, the run function has ended, and the "edit" object isn't valid  anymore. Problem is that we need it to insert text in the new view.
   def save_class(self, className):
     self.view.run_command("gold_do_save_class", {"className": className})


class GoldDoSaveClassCommand(sublime_plugin.TextCommand):

   def run(self, edit, className):
      
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

      result = ctypes.c_char_p( gold_environnement.hWamAPI.execEwamCmd(0, request) )
      print(result.value.decode('ascii'))
      jsonObj = json.loads(result.value.decode('ascii'))
      
      newView = sublime.active_window().new_file()

      newView.set_scratch(True)
      newView.set_name(className + ".gold")
      newView.insert(edit, 0, jsonObj['eWamReply']['myResult'].replace('\r\n', '\n'))
      #newView.insert(edit, 0, jsonObj['eWamReply']['myResult'])

      # Probably rather use 'Packages/Gold/gold.tmLanguage' : consider the user has installed the plugin package 'Gold'
      newView.set_syntax_file('Packages/User/gold.tmLanguage')
      gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)

      