import sublime, sublime_plugin, User.gold_environnement, User.gold_helpers

class GoldNewEnvProjCommand(sublime_plugin.ApplicationCommand):

    def run(self):
        User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
        sublime.active_window().run_command("new_window")
        sublime.message_dialog("You will be asked to select the root diretory of the  eWAM\nenvironnement you want to use, and where the corresponding\nproject will be saved.")
        sublime.active_window().run_command("save_project_as")
        projectFilename = sublime.active_window().project_file_name()

        if projectFilename != None:
            projectPath = projectFilename[0:projectFilename.rfind('\\')]
            User.gold_environnement.InitializeEnvironnement(projectPath)
            sublime.active_window().set_project_data({ "wyde-root": projectPath })

        User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
