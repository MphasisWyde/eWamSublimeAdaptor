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
   viewname = view.name()
   filename = view.file_name()
   name = ""

   if filename == None:
      if viewname == None:
         return False
      else:
         name = viewname
   else:
      name = filename

   return name.rfind(".gold") == len(name)-5 or name.rfind(".god") == len(name)-4

def LogMessage(message):
   print("Gold Plugin: " + message)

def LogAndStatusMessage(message):
   LogMessage(message)
   sublime.status_message(message)