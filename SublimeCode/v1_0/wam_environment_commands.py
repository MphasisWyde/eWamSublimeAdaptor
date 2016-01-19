import sublime, sublime_plugin, sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "plugin"))
import environment

class WamNewEnvCommand(sublime_plugin.ApplicationCommand):

   # def is_enabled(self):
   #    return True

   # def is_visible(self):
   #    return True

   # def is_checked(self):
   #    return False

   def description(self):
      return "Add a new environment in your settings"

   def run(self):
      sublime.active_window().show_input_panel("Environment URL:", "http://localhost:8082", self.done_panel_env_url, None, None)

   def done_panel_env_url(self, env_url):
      self.env_url = env_url
      sublime.active_window().show_input_panel("Environment name:", "Wynsure 5.6", self.done_panel_env_name, None, None)

   def done_panel_env_name(self, name):
      self.name = name
      environment.save_environment(self.name, self.env_url)


class WamClearEnvsCommand(sublime_plugin.ApplicationCommand):

   # def is_enabled(self):
   #    return True

   # def is_visible(self):
   #    return True

   # def is_checked(self):
   #    return False

   def description(self):
      return "Clears your environments"

   def run(self):
      environment.clear_environments()
      environment.reset_working_environment()


class WamRenameEnvCommand(sublime_plugin.ApplicationCommand):

   # def is_enabled(self):
   #    return True

   # def is_visible(self):
   #    return True

   # def is_checked(self):
   #    return False

   def description(self):
      return "Rename an eWam environment"

   def run(self):
      pass


class WamSelectEnvCommand(sublime_plugin.WindowCommand):

   # def is_enabled(self):
   #    return True

   # def is_visible(self):
   #    return True

   def description(self):
      return "Select an environment"

   def run(self):
      environment.select_environment(self.window, environment.set_working_environment)



class WamRemoveEnvCommand(sublime_plugin.WindowCommand):

   # def is_enabled(self):
   #    return True

   # def is_visible(self):
   #    return True

   def description(self):
      return "Remove an environment"

   def run(self):
      environment.select_environment(self.window, environment.remove_environment)
