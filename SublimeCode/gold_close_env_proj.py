import sublime, sublime_plugin, User.gold_environnement, User.gold_helpers, sys

class GoldCloseEnvProjCommand(sublime_plugin.ApplicationCommand):

    def run(self):
        User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)

        sublime.active_window().run_command("close_project")

        User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)

    def is_enabled(self):
        return User.gold_helpers.IsGoldProjectLoaded()
