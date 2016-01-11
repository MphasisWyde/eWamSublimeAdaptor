import sublime, sublime_plugin, sys
from . import gold_helpers

class GoldOpenEnvProjCommand(sublime_plugin.ApplicationCommand):

    def run(self):
        gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
        sublime.active_window().run_command("open_window")
        sublime.active_window().run_command("prompt_open_project")
        projectFilename = sublime.active_window().project_file_name()
        projectPath = sublime.active_window().project_data()['wyde-root']

        if projectFilename != None and projectPath != None:
            # projectPath = projectFilename[0:projectFilename.rfind('\\')]
            gold_environnement.InitializeEnvironnement(projectPath)

        gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
