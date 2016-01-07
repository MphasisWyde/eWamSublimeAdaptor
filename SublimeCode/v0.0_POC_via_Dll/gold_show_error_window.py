import sublime, sublime_plugin, sys
from . import *

class GoldShowErrorWindowCommand(sublime_plugin.ApplicationCommand):

   def run(self):
      gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + sys._getframe().f_code.co_name)

      if gold_environnement.goldErrorsView == None:
         gold_environnement.InitializeErrorList()

      sublime.active_window().run_command("show_panel", { 'panel': 'output.golderrors' })

      gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + sys._getframe().f_code.co_name)