import sublime

def AlertError(message):
   print("Gold Plugin error:", message)
   sublime.error_message("Gold Plugin error: " + message)

def LogError(message):
   print("Gold Plugin error:", message)

def IsAGoldView(view=None):
   if view == None:
      view = sublime.active_window().active_view()

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

def get_view_name(view=None):
   if view == None:
      view = sublime.active_window().active_view()
      
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

   return name.split('.')[0]

def get_module_from_view(view=None):
   name = get_view_name(view)
   path = name.split('\\')
   name = path[len(path)-1]
   return name

def get_view_content(view=None):
   if view == None:
      view = sublime.active_window().active_view()

   return view.substr(sublime.Region(0, view.size()))