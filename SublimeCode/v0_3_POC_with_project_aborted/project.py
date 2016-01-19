import sublime, sublime_plugin, sys
from . import plugin_helpers


wamProject = None



class WamEnvironment:
   base_url = ""
   name = ""

   def __init__(self, baseurl, name):
      self.base_url = baseurl
      self.name = name

   def getDict(self):
      return   {  
                  "environment":
                  [
                     { "base_url": self.base_url }, 
                     { "name": self.name }
                  ]
               }



class WamProject:
   environment = None
   window = None

   def __init__(self, env, wnd):
      self.environment = env
      self.window = wnd

   def getDict(self):
      return   {  
                  "wam":
                  [ self.environment.getDict() ]
               }

   def save(self):
      print(self.getDict())
      self.window.set_project_data(self.getDict())


""" Create and initilize project and eWam environment
"""
class WamProjectInitCommand(sublime_plugin.WindowCommand):

   def is_enabled(self):
      return True

   def is_visible(self):
      return True

   def description(self):
      return "Open an eWAM environment in a new workspace"

   def run(self):
      plugin_helpers.DebugLogMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)

      sublime.message_dialog("Please provide the URL to this environment.")
      self.window.show_input_panel("Environment base URL:", "http://localhost:8082", self.save_project_as, None, None)

      plugin_helpers.DebugLogMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)

   def save_project(self, env_url):
      plugin_helpers.DebugLogMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)

      sublime.message_dialog("Please choose a path and name for this new workspace.")
      self.window.run_command("save_project_as")

      newEnv = WamEnvironment(env_url)
      wamProject = WamProject(newEnv, self.window)

      if wamProject != None:
         wamProject.save()

      plugin_helpers.DebugLogMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)