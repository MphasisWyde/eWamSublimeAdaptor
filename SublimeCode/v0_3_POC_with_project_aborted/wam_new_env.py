import sublime, sublime_plugin, sys
from . import plugin_helpers

class WamNewEnvCommand(sublime_plugin.ApplicationCommand):

   # def is_enabled(self):
   #    return True

   # def is_visible(self):
   #    return True

   # def is_checked(self):
   #    return False

   def description(self):
      return "Open en eWAM environment in a new workspace"

   def run(self):
      plugin_helpers.DebugLogMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)

      # sublime.active_window().run_command("new_window")
      # sublime.active_window().run_command("wam_project_init")

      print(sublime.cache_path())

      plugin_helpers.DebugLogMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)


