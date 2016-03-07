import sublime_plugin
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "plugin"))
sys.path.append(os.path.join(os.path.dirname(__file__), "third-party"))

import bravado
import helpers
import environment
import actions
import inputs

class WamNewClassCommand(sublime_plugin.WindowCommand):

   def is_enabled(self):
      return True

   def is_visible(self):
      return True

   def description(self):
      return "Create a new class"

   def run(self):
      inputs.get_user_input(self.classname_chosen, "Choose a class name:")

   def classname_chosen(self, name):
      self.classname = name
      inputs.get_class_or_module_name(self.ancestorname_chosen, "Search for ancestor:")

   def ancestorname_chosen(self, name):
      self.ancestorname = name

      classImplem = "; " + self.classname + " (" + self.ancestorname + ") (Def Version:1) (Implem Version:1)" + "\n\n" + "class " + self.classname + " (" + self.ancestorname + ")\n"
      classImplem = classImplem.replace('\n', "\\r\\n")

      api = environment.getSwaggerAPI()
      implemModel = api.get_model("tImplem")
      implem = implemModel(content=classImplem, name=self.classname, ancestor=self.ancestorname)

      res = api.ModuleDefAPI.ModuleDefAPI_Create(body=implem).result()

      res = api.ModuleDefAPI.ModuleDefAPI_Get(name=self.classname).result()
      newView = actions.open_gold_window(res['name'], res['content'])


class WamNewModuleCommand(sublime_plugin.WindowCommand):

   def is_enabled(self):
      return False

   def is_visible(self):
      return True

   def description(self):
      return "Create a new module"

   def run(self):
      inputs.get_user_input(self.classname_chosen, "Choose a module name:")

   def classname_chosen(self, name):
      self.modulename = name

      moduleImplem = "; " + self.modulename + "(Def Version:1) (Implem Version:1)" + "\n\n" + "module " + self.modulename + "\n"
      moduleImplem = moduleImplem.replace('\n', "\\r\\n")

      api = environment.getSwaggerAPI()
      implemModel = api.get_model("tImplem")
      implem = implemModel(content=moduleImplem, name=self.modulename, ancestorname="")

      res = api.ModuleDefAPI.ModuleDefAPI_Create(body=implem).result()

      res = api.ModuleDefAPI.ModuleDefAPI_Get(name=self.modulename).result()
      newView = actions.open_gold_window(res['name'], res['content'])


class WamParseCommand(sublime_plugin.TextCommand):

   def is_enabled(self):
      return helpers.is_a_gold_view(self.view)

   def is_visible(self):
      return helpers.is_a_gold_view(self.view)

   def description(self):
      return "Parse class or module"

   def want_event(self):
      return False

   def run(self, edit, event=None, refresh=True):
      moduleName = helpers.get_module_from_view(self.view)

      if not helpers.is_entity_checkedout(moduleName):
         return
         
      api = environment.getSwaggerAPI()

      implemModel = api.get_model("tImplem")
      content = helpers.get_view_content(self.view)

      content = content.replace('\n', "\\r\\n")

      implem = implemModel(content=content, name=moduleName, ancestor="")

      res = api.ModuleDefAPI.ModuleDefAPI_Parse(name=moduleName, body=implem).result()

      actions.update_error_view(res['errors'], self.view)

      if len(res['errors']) == 0 and refresh:
         actions.update_content(self.view, res['content'])

class WamSaveCommand(sublime_plugin.TextCommand):

   def is_enabled(self):
      return helpers.is_a_gold_view(self.view)

   def is_visible(self):
      return helpers.is_a_gold_view(self.view)

   def description(self):
      return "Save class or module"

   def want_event(self):
      return False

   def run(self, edit, event=None, refresh=True):
      api = environment.getSwaggerAPI()

      implemModel = api.get_model("tImplem")
      content = helpers.get_view_content(self.view)
      moduleName = helpers.get_module_from_view(self.view)

      content = content.replace('\n', "\\r\\n")

      implem = implemModel(content=content, name=moduleName, ancestor="")

      res = api.ModuleDefAPI.ModuleDefAPI_Modify(name=moduleName, body=implem).result()

      actions.update_error_view(res['errors'], self.view)

      if len(res['errors']) == 0 and refresh:
         actions.update_content(self.view, res['content'])

class WamGetScenarioCommand(sublime_plugin.TextCommand):

   def is_enabled(self):
      return helpers.is_a_gold_view(self.view)

   def is_visible(self):
      return helpers.is_a_gold_view(self.view)

   def description(self):
      return "Get a scenario"

   def want_event(self):
      return False

   def run(self, edit, event=None, refresh=True):
      api = environment.getSwaggerAPI()

      moduleName = helpers.get_module_from_view(self.view)
      inputs.choose_scenario(self.inputResultCallback, view=self.view)

   def inputResultCallback(self, scenario):
      api = environment.getSwaggerAPI()
      moduleName = helpers.get_module_from_view(self.view)
      res = api.ModuleDefAPI.ModuleDefAPI_GetMyScenario(name=moduleName, scenarioName=scenario['label']).result()
      
class WamCheckoutCommand(sublime_plugin.TextCommand):

   def is_enabled(self):
      name = helpers.get_module_from_view(self.view)
      return not helpers.is_entity_checkedout(name)

   def is_visible(self):
      name = helpers.get_module_from_view(self.view)
      return not helpers.is_entity_checkedout(name)

   def description(self):
      return "Checkout the module"

   def want_event(self):
      pass

   def run(self, edit):
      api = environment.getSwaggerAPI()

      name = helpers.get_module_from_view(self.view)
      res = api.ModuleDefAPI.ModuleDefAPI_CheckOut(name=name).result()
      actions.update_readonly(self.view)

class WamCheckinCommand(sublime_plugin.TextCommand):

   def is_enabled(self):
      name = helpers.get_module_from_view(self.view)
      return helpers.is_entity_checkedout(name)

   def is_visible(self):
      name = helpers.get_module_from_view(self.view)
      return helpers.is_entity_checkedout(name)

   def description(self):
      return "Check-in the module"

   def want_event(self):
      pass

   def run(self, edit):
      api = environment.getSwaggerAPI()

      name = helpers.get_module_from_view(self.view)
      res = api.ModuleDefAPI.ModuleDefAPI_CheckIn(name=name).result()
      actions.update_readonly(self.view)

class WamDeliverCommand(sublime_plugin.TextCommand):

   def is_enabled(self):
      name = helpers.get_module_from_view(self.view)
      return helpers.is_entity_checkedout(name)

   def is_visible(self):
      name = helpers.get_module_from_view(self.view)
      return helpers.is_entity_checkedout(name)

   def description(self):
      return "Deliver the module"

   def want_event(self):
      pass

   def run(self, edit):
      api = environment.getSwaggerAPI()
      name = helpers.get_module_from_view(self.view)
      res = api.ModuleDefAPI.ModuleDefAPI_Deliver(name=name).result()
      actions.update_readonly(self.view)
