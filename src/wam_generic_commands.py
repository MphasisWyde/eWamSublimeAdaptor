import sublime
import sublime_plugin
import sys, os, re

sys.path.append(os.path.join(os.path.dirname(__file__), "plugin"))
sys.path.append(os.path.join(os.path.dirname(__file__), "third-party"))

import environment
import helpers
import actions
import inputs
import bravado


class WamSwaggerGenericCallCommand(sublime_plugin.WindowCommand):

   swaggerAPI = None
   operationId = ""
   operation = None
   parameters = None
   actionName = ""
   action = None
   paramBeingTreated = None
   currentMatch = None
   dummyresult = None
   opresult = None

   def is_enabled(self):
      return True

   def is_visible(self):
      return True

   def description(self):
      return "Call through swagger API"

   def run(self, operationId, params={}, action=""):
      self.swaggerAPI = environment.getSwaggerAPI()
      if self.swaggerAPI == None:
         return

      if operationId == None or operationId == "":
         helpers.log_error("'operationId' not provided")
         return

      self.operationId = operationId
      self.setOperationFromId()

      self.parameters = params
      self.action = action

      # Start parsing parameters
      self.expandParams()

   def expandParams(self):
      tagRegex = re.compile(r"<<[^>]+>>")

      dummyToTreat = False
      if 'dummy' in self.parameters:
         match = tagRegex.search(self.parameters['dummy'])
         if match != None:
            dummyToTreat = True

      for param in self.parameters:
         if dummyToTreat and param != 'dummy':
            continue

         match = tagRegex.search(self.parameters[param])
         if match == None:
            # Nothing left to expand in this parameter
            pass
         else:
            self.paramBeingTreated = param
            self.currentMatch = match
            replacor = self.parameters[param][match.start()+2:match.end()-2]
            
            sublime.set_timeout_async(exec(replacor, globals(), locals()), 10)
            # We will be waiting for the method to call back doneInputOneTag
            return

      self.executeCommand()

   def inputResultCallback(self, expandedValue):
      if isinstance(expandedValue, str):
         oldValue = self.parameters[self.paramBeingTreated]
         self.parameters[self.paramBeingTreated] = oldValue[:self.currentMatch.start()] + expandedValue + oldValue[self.currentMatch.end():]
      elif isinstance(expandedValue, dict):
         self.dummyresult = expandedValue
         oldValue = self.parameters[self.paramBeingTreated]
         self.parameters[self.paramBeingTreated] = oldValue[:self.currentMatch.start()] + oldValue[self.currentMatch.end():]

      self.expandParams()

   def executeOperation(self):
      try:
         if self.operation != None:
            if 'dummy' in self.parameters:
               del self.parameters['dummy']
            kwargs = self.parameters
            self.opresult = self.operation(**kwargs).result()
      except bravado.exception.HTTPError as e:
         self.opresult = None
         helpers.log_error(e)

   def setOperationFromId(self):
      # We expect operationId to be the one specified in swagger documentation
      # e.g.: ModuleDefAPI_Get
      moduleName = self.operationId.split('_')[0]
      module = getattr(self.swaggerAPI, moduleName)
      if module == None:
         helpers.log_error("Module '" + moduleName + "' not found, deduced from '" + self.operationId + "'. [" + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + "]")

      self.operation = getattr(module, self.operationId)
      if self.operation == None:
         helpers.log_error("Operation '" + self.operationId + "' not found. [" + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + "]")

   def executeAction(self):
      response = self.opresult
      exec(self.action, globals(), locals())

   def executeCommand(self):
      self.executeOperation()
      self.executeAction()

class WamSwaggerGoldGenericCallCommand(WamSwaggerGenericCallCommand):

   def is_enabled(self):
      return helpers.is_a_gold_view(self.view)

   def is_visible(self):
      return helpers.is_a_gold_view(self.view)

class WamSwaggerGenericContextualCallCommand(sublime_plugin.TextCommand):

   swaggerAPI = None
   operationId = ""
   operation = None
   parameters = None
   actionName = ""
   action = None
   paramBeingTreated = None
   currentMatch = None

   x = -1
   y = -1
   selectedTextPoint = (-1, -1)
   selectedWordRegions = None
   selectedWord = ""

   dummyresult = None
   opresult = None

   def is_enabled(self):
      return helpers.is_a_gold_view(self.view)

   def is_visible(self):
      return helpers.is_a_gold_view(self.view)

   def description(self):
      return "Open en eWAM environment in a new workspace"

   def want_event(self):
      return True

   def run(self, edit, event, operationId, params={}, action=""):

      self.x = int(event["x"])
      self.y = int(event["y"])

      self.selectedTextPoint = self.view.window_to_text((self.x, self.y))
      self.selectedWordRegions = self.view.word(self.selectedTextPoint)
      self.selectedWord = self.view.substr(self.selectedWordRegions)

      self.swaggerAPI = environment.getSwaggerAPI()

      if self.swaggerAPI == None:
         return

      if operationId == None or operationId == "":
         helpers.log_error("'operationId' not provided")
         return

      self.operationId = operationId
      self.setOperationFromId()

      self.parameters = params
      self.action = action

      # Start parsing parameters
      self.expandParams()

   def expandParams(self):
      tagRegex = re.compile(r"<<[^>]+>>")

      dummyToTreat = False
      if 'dummy' in self.parameters:
         match = tagRegex.search(self.parameters['dummy'])
         if match != None:
            dummyToTreat = True

      for param in self.parameters:
         if dummyToTreat and param != 'dummy':
            continue

         match = tagRegex.search(self.parameters[param])
         if match == None:
            # Nothing left to expand in this parameter
            pass
         else:
            self.paramBeingTreated = param
            self.currentMatch = match
            replacor = self.parameters[param][match.start()+2:match.end()-2]
            
            sublime.set_timeout_async(exec(replacor, globals(), locals()), 10)
            # We will be waiting for the method to call back doneInputOneTag
            return

      self.executeCommand()

   def inputResultCallback(self, expandedValue):
      if isinstance(expandedValue, str):
         oldValue = self.parameters[self.paramBeingTreated]
         self.parameters[self.paramBeingTreated] = oldValue[:self.currentMatch.start()] + expandedValue + oldValue[self.currentMatch.end():]
      elif isinstance(expandedValue, dict):
         self.dummyresult = expandedValue
         oldValue = self.parameters[self.paramBeingTreated]
         self.parameters[self.paramBeingTreated] = oldValue[:self.currentMatch.start()] + oldValue[self.currentMatch.end():]

      self.expandParams()

   def executeOperation(self):
      try:
         if self.operation != None:
            if 'dummy' in self.parameters:
               del self.parameters['dummy']
            kwargs = self.parameters
            self.opresult = self.operation(**kwargs).result()
      except bravado.exception.HTTPError as e:
         self.opresult = None
         helpers.log_error(e)

   def setOperationFromId(self):
      # We expect operationId to be the one specified in swagger documentation
      # e.g.: ModuleDefAPI_Get
      moduleName = self.operationId.split('_')[0]
      module = getattr(self.swaggerAPI, moduleName)
      if module == None:
         helpers.log_error("Module '" + moduleName + "' not found, deduced from '" + self.operationId + "'. [" + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + "]")

      self.operation = getattr(module, self.operationId)
      if self.operation == None:
         helpers.log_error("Operation '" + self.operationId + "' not found. [" + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + "]")

   def executeAction(self):
      response = self.opresult
      exec(self.action, globals(), locals())

   def executeCommand(self):
      self.executeOperation()
      self.executeAction()
