import sublime_plugin, sys
from . import gold_helpers

# class SaveCommand(sublime_plugin.TextCommand):

# 	def run(self, edit):
# 		gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)

# 		# self.view.run_command("save")

# 		gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
