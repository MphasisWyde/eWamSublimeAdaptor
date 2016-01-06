import sublime

def IsGoldProjectLoaded():
   projName = sublime.active_window().project_file_name()
   if projName == None:
      return False

   if sublime.active_window().project_data()['wyde-root'] != None:
      return True
   else:
      return False

def IsGoldCode(view):
   filename = view.name()
   if filename == None:
      return False
  
   splitname = filename.split('.')
   extension = splitname[len(splitname) - 1]
   return extension == "gold" or extension == "god"

def LogMessage(message):
   print("Gold Plugin: " + message)

def LogAndStatusMessage(message):
   LogMessage(message)
   sublime.status_message(message)