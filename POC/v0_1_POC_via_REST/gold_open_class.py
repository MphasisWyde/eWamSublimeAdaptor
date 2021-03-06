import sublime, sublime_plugin, ctypes, json, sys, http.client
from . import gold_helpers

class GoldOpenClassCommand(sublime_plugin.TextCommand):

   def run(self, edit):
      gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
      # Callback "open_class" when name has been entered
      sublime.active_window().show_input_panel("Enter class name:", "", self.open_class, None, None)

   # Forward call to another command that will actually create a new view. We are forced to do this because at the time this callback is called, the run function has ended, and the "edit" object isn't valid  anymore. Problem is that we need it to insert text in the new view.
   def open_class(self, className):
     self.view.run_command("gold_do_open_class", {"className": className})


class GoldDoOpenClassCommand(sublime_plugin.TextCommand):

   def run(self, edit, className):
      conn = http.client.HTTPConnection('localhost:8082')

      conn.request("GET", "/aeWamManager/openentity/"+className)
      resp = conn.getresponse()

      if resp.status == 200:
         newView = sublime.active_window().new_file()
         newView.set_scratch(True)
         newView.set_name(className + ".gold")
         newView.insert(edit, 0, resp.read().decode("ascii").replace('\r\n', '\n'))
         newView.set_syntax_file('Packages/Gold/gold.tmLanguage')
      #elif resp.status == 404:
      #  self.view.run_command("gold_do_open_class", {"className": className})
          

      print(resp.status, resp.reason, resp.read())
      conn.close()

      gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)