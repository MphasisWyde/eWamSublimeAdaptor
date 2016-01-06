import sublime, sublime_plugin, User.gold_helpers, User.gold_environnement, sys

class GoldShowErrorWindowCommand(sublime_plugin.ApplicationCommand):

   def run(self):
      User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + sys._getframe().f_code.co_name)

      if User.gold_environnement.goldErrorsView == None:
         User.gold_environnement.InitializeErrorList()

      sublime.active_window().run_command("show_panel", { 'panel': 'output.golderrors' })

      User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + sys._getframe().f_code.co_name)