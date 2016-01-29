import sublime, sublime_plugin, sys, os, re

sys.path.append(os.path.join(os.path.dirname(__file__), "plugin"))
sys.path.append(os.path.join(os.path.dirname(__file__), "third-party"))
import environment
import helpers
import actions
import inputs


class WamSwaggerGenericCallCommand(sublime_plugin.WindowCommand):

   swaggerAPI = None
   operationId = ""
   operation = None
   parameters = None
   actionName = ""
   action = None
   paramBeingTreated = None
   currentMatch = None

   def is_enabled(self):
      return True

   def is_visible(self):
      return True

   def description(self):
      return "Call through swagger API"

   def run(self, operationId, params, action):
      self.swaggerAPI = environment.getSwaggerAPI()
      if self.swaggerAPI == None:
         return

      if operationId == None or operationId == "":
         helpers.LogError("'operationId' not provided")
         return

      self.operationId = operationId
      self.setOperationFromId()

      self.parameters = params
      self.action = action

      # Start parsing parameters
      self.expandParams()

   def expandParams(self):
      tagRegex = re.compile(r"<<[^>]+>>")

      for param in self.parameters:
         match = tagRegex.search(self.parameters[param])
         if match == None:
            # Nothing left to expand in this parameter
            pass
         else:
            self.paramBeingTreated = param
            self.currentMatch = match
            replacor = self.parameters[param][match.start()+2:match.end()-2]

            replacor += "(self.doneInputOneTag)"
            sublime.set_timeout_async(eval(replacor, globals(), locals()), 10)
            # We will be waiting for the method to call back doneInputOneTag
            return

      self.executeCommand()

   def doneInputOneTag(self, expandedValue):
      oldValue = self.parameters[self.paramBeingTreated]
      self.parameters[self.paramBeingTreated] = oldValue[:self.currentMatch.start()] + expandedValue + oldValue[self.currentMatch.end():]
      self.expandParams()

   def executeOperation(self):
      if self.operation != None:
         kwargs = self.parameters
         self.result = self.operation(**kwargs).result()

   def setOperationFromId(self):
      # We expect operationId to be the one specified in swagger documentation
      # e.g.: ModuleDefAPI_Get
      moduleName = self.operationId.split('_')[0]
      module = getattr(self.swaggerAPI, moduleName)
      if module == None:
         helpers.LogError("Module '" + moduleName + "' not found, deduced from '" + self.operationId + "'. [" + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + "]")

      self.operation = getattr(module, self.operationId)
      if self.operation == None:
         helpers.LogError("Operation '" + self.operationId + "' not found. [" + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + "]")


      # Use if we want several levels of encapsulation of modules
      # for moduleName in modules:
      #    module = getattr(module, moduleName)
      # method = module

   # def setActionFromName(self):
   #    # Find and call action method
   #    actionPath = self.actionName.split('.')
   #    module = globals()[actionPath[0]]
   #    for moduleName in actionPath[1:]:
   #       if module == None:
   #          helpers.LogError("Module '" + moduleName + "' not found, deduced from '" + self.actionName + "'. [" + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + "]")
   #          break

   #       module = getattr(module, moduleName)

   #    self.action = module
   #    if self.action == None:
   #       helpers.LogError("Action '" + self.actionName + "' not found. [" + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + "]")

   def executeAction(self):
      response = self.result
      exec(self.action, globals(), locals())

   def executeCommand(self):
      self.executeOperation()
      self.executeAction()


            












