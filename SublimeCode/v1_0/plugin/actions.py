import sublime
import time
import environment
import helpers

def update_content(view=None, content=""):
   if view == None:
      view = sublime.active_window().active_view()
   
   view.run_command("wam_insert_text", {"text": content.replace('\r\n', '\n') })
   return view

def open_window(name="", content=""):
   newView = sublime.active_window().new_file()

   while newView.is_loading():
      time.sleep(0.1)

   newView.set_name(name)
   update_content(newView, content)
   return newView

def open_gold_window(name="", content=""):
   newView = open_window(name, content)

   newView.set_scratch(True)
   newView.set_name(name + ".gold")

   newView.set_syntax_file('Packages/Gold/gold.tmLanguage')
   return newView

def update_readonly(view=None):
   if view == None:
      view = sublime.active_window().active_view()

   module_name = helpers.get_module_from_view(view)

   api = environment.getSwaggerAPI()
   status = api.ModuleDefAPI.ModuleDefAPI_entityStatus(name=module_name).result()
   view.set_read_only(not status.checkedOut)

