import sublime, sublime_plugin, ctypes, json, User.gold_environnement, sys, http.client

class GoldSearchEntityCommand(sublime_plugin.TextCommand):

   def run(self, edit):
      User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
      # Callback "open_class" when name has been entered
      sublime.active_window().show_input_panel("Enter entity name:", "", self.search_entity, None, None)

   

   # Forward call to another command that will actually create a new view. We are forced to do this because at the time this callback is called, the run function has ended, and the "edit" object isn't valid  anymore. Problem is that we need it to insert text in the new view.
   def search_entity(self, className):
     self.view.run_command("gold_do_search_entity", {"className": className})


class GoldDoSearchEntityCommand(sublime_plugin.TextCommand):

   def run(self, edit, className):
      conn = http.client.HTTPConnection('localhost:8082')

      conn.request("GET", "/aeWamManager/searchEntities/"+className)
      resp = conn.getresponse()
      newView = sublime.active_window().new_file()

      #newView.set_scratch(True)
      newView.set_name(className + ".gold")
      newView.insert(edit, 0, resp.read().decode("ascii").replace('\r\n', '\n'))
      #newView.insert(edit, 0, jsonObj['eWamReply']['myResult'])


      print(resp.status, resp.reason, resp.read())
      conn.close()

      User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)