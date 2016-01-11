import sublime, sublime_plugin, sys
from . import gold_environnement, gold_helpers

class GoldCloseEnvProjCommand(sublime_plugin.ApplicationCommand):

    def run(self):
        gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)

        sublime.active_window().run_command("close_project")

        gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)

    def is_enabled(self):
        return gold_helpers.IsGoldProjectLoaded()
