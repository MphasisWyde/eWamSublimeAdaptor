import sublime
import sublime_plugin
import sys, os, re, json

sys.path.append(os.path.join(os.path.dirname(__file__), "plugin"))
sys.path.append(os.path.join(os.path.dirname(__file__), "third-party"))

import environment
import helpers
import inputs
import actions
import bravado

class WamGotoDefinitionCommand(sublime_plugin.TextCommand):

   def run(self, edit, event):

      x = int(event["x"])
      y = int(event["y"])

      self.selectedTextPoint = self.view.window_to_text((x, y))
      self.selectedWordRgn = self.view.word(self.selectedTextPoint)
      self.selectedWord = self.view.substr(self.selectedWordRgn)
      inputs.searchEntity(self.entity_chosen, self.selectedWord)

   def is_enabled(self):
      return helpers.IsAGoldView(self.view)

   def is_visible(self):
      return helpers.IsAGoldView(self.view)

   def want_event(self):
      return True

   def entity_chosen(self, picked):
      self.api = environment.getSwaggerAPI()
      # print(self.api.EntityAPI.EntityAPI_GetEntity(name=picked.name, ownerName="aRedgisTest").result())
      entity = self.api.EntityAPI.EntityAPI_GetEntity(name=picked['name'], ownerName="aRedgisTest").result()
      
      actions.open_gold_window(picked['name'], json.dumps(entity))

      # self.view.window().run_command("wam_swagger_generic_call", { "operationId" : "EntityAPI_GetEntity", "params" : { "name": picked['name'], "ownerName": "aRedgisTest" }, "action" : "import json; actions.open_gold_window(json.dumps(response))" })
        