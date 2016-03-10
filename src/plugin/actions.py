import sublime
import time
import environment
import helpers
import json

def update_content(view=None, content=""):
   if view == None:
      view = sublime.active_window().active_view()
   
   # view.run_command("wam_clear_text")
   # view.run_command("wam_insert_text", {"text": content.replace('\r\n', '\n') })
   view.run_command("wam_replace_text", {"text": content.replace('\r\n', '\n') })
   view.sel().clear()
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

   newView.set_syntax_file('Packages/Gold/gold.sublime-syntax')
   return newView

def update_readonly(view=None):
   if view == None:
      view = sublime.active_window().active_view()

   if not helpers.is_a_gold_view(view):
      return

   module_name = helpers.get_module_from_view(view)

   api = environment.getSwaggerAPI()
   status = api.ModuleDefAPI.ModuleDefAPI_entityStatus(name=module_name).result()
   view.set_read_only(not status['checkedOut'])

def open_entity(name, entity):
   if entity['theType'] == "aClassDef" or entity['theType'] == "aModuleDef":
      api = environment.getSwaggerAPI()
      module = api.ModuleDefAPI.ModuleDefAPI_Get(name=name).result()
      open_gold_window(name=name, content=module['content'])
   else:
      view = open_window(name=name+".gold", content=json.dumps(entity, indent=3))
      view.set_syntax_file('Packages/JavaScript/JSON.tmLanguage')
      view.set_scratch(True)

def update_error_view(errors, view=None):
   if view == None:
      view = sublime.active_window().active_view()

   # Initialize and show error window
   errorView = view.window().create_output_panel('gold_error_panel', True)
   errorView.set_read_only(False)
   errorView.run_command("wam_clear_text")

   if len(errors) == 0:
      view.erase_regions('errors')
      return

   # Clear error decorations
   errRegions = []
   lineRegions = view.split_by_newlines(sublime.Region(0, view.size()))

   for error in errors:
      errRegions += [lineRegions[error['line']]]

      message = view.name() + ":" + str(error['line']) + ":" + str(error['offSet']) + ":" + error['msg'] + "\n"
      errorView.run_command("wam_append_text", { 'text': message } )

   # Add error decorations
   view.add_regions('errors', errRegions, 'invalid', 'Packages/Gold/dot.png', sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE | sublime.DRAW_SQUIGGLY_UNDERLINE)

   errorView.set_read_only(True)

   sublime.active_window().run_command("show_panel", { 'panel': 'output.gold_error_panel' })