import sublime

for window in sublime.windows():
   # Is there an eWAM environment associated with this window ?
   prjdata = window.project_data()
   env = prjdata['WamEnvironment']
   
   # Yes ? => Restore the edits
   if env != None:
      pass
