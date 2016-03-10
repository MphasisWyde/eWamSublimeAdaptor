import sublime, sublime_plugin, os.path

class WamCheckFolderCommand(sublime_plugin.WindowCommand):

   # def is_enabled(self):
   #    return True

   # def is_visible(self):
   #    return True

   def description(self):
      return "Folders ?"

   def run(self):
      for folder in self.window.folders():
         print(os.listdir(folder))
   
