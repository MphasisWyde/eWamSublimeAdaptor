import sublime_plugin
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "plugin"))
sys.path.append(os.path.join(os.path.dirname(__file__), "third-party"))

import bravado
import helpers
import environment
import actions
import inputs

class WamRunMethodCommand(sublime_plugin.TextCommand):

   def is_enabled(self):
      return helpers.is_a_gold_view(self.view)

   def is_visible(self):
      return helpers.is_a_gold_view(self.view)

   def description(self):
      return "Run method"

   def want_event(self):
      return True

   def run(self, edit, event=None):
      moduleName = helpers.get_module_from_view(self.view)

      if not helpers.is_entity_checkedout(moduleName):
         return

      x = int(event["x"])
      y = int(event["y"])

      word = helpers.get_word_at(x, y, self.view)
      if word == None or word == "":
         return

      classname = helpers.get_module_from_view(self.view)

      api = environment.getSwaggerAPI()

      res = api.Runner.Runner_RunClassMethod(className=classname, methodName=word).result()



class WamRunClassCommand(sublime_plugin.TextCommand):

   def is_enabled(self):
      return helpers.is_a_gold_view(self.view)

   def is_visible(self):
      return helpers.is_a_gold_view(self.view)

   def description(self):
      return "Run class"

   def want_event(self):
      return True

   def run(self, edit, event=None):
      moduleName = helpers.get_module_from_view(self.view)

      if not helpers.is_entity_checkedout(moduleName):
         return

      x = int(event["x"])
      y = int(event["y"])

      word = helpers.get_word_at(x, y, self.view)
      if word == None or word == "":
         return

      classname = helpers.get_module_from_view(self.view)

      api = environment.getSwaggerAPI()

      res = api.Runner.Runner_RunClass(className=classname).result()

