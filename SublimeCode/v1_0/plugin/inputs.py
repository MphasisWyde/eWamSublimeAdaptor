import sublime
import environment
import helpers
import input_handler


""" Class name retrieving from user input
"""
def get_class_or_module_name(callback, label="Enter class name:"):
   inputHandler = input_handler.TextInputHandler(finalcallback=callback, inputDone=on_classname_input_done)
   inputHandler.input_text(label)

def on_classname_input_done(inputHandler, text):
   api = environment.getSwaggerAPI()

   fullChoiceList = api.MMBrowserAPI.MMBrowserAPI_searchEntities(q=text, _class="true", _module="true").result()
   
   lightChoiceList = []
   for item in fullChoiceList:
      if item['ownerName'] == "nil" or item['ownerName'] == "":
         lightChoiceList.append([item['label'] + " : " + item['description']])
      else:
         lightChoiceList.append([item['label'] + " : " + item['description'], item['ownerName'] ])

   choiceHandler = input_handler.ChoiceInputHandler(finalcallback=inputHandler.finalcallback, selectionDone=on_class_chosen, fullChoiceList=fullChoiceList, lightChoiceList=lightChoiceList)

   choiceHandler.choice_input()

def on_class_chosen(choiceHandler, selectedRank):
   choiceHandler.finalcallback(choiceHandler.fullChoiceList[selectedRank]['label'])

# End of class name retrieval

def get_user_input(callback, label="Input:"):
   textInputHandler = input_handler.TextInputHandler(finalcallback=callback, inputDone=userinput_done)
   textInputHandler.input_text(label)

def userinput_done(textInputHandler, inputResult):
   textInputHandler.finalcallback(inputResult)

def searchEntity(callback, name):
   api = environment.getSwaggerAPI()
   fullChoiceList = api.MMBrowserAPI.MMBrowserAPI_searchEntities(q=name).result()

   lightChoiceList = []
   for item in fullChoiceList:
      if item['ownerName'] == "nil" or item['ownerName'] == "":
         lightChoiceList.append([item['label'] + " : " + item['description']])
      else:
         lightChoiceList.append([item['label'] + " : " + item['description'], item['ownerName'] ])

   choiceHandler = input_handler.ChoiceInputHandler(finalcallback=callback, selectionDone=entityChosen, fullChoiceList=fullChoiceList, lightChoiceList=lightChoiceList)

   choiceHandler.choice_input()

def entityChosen(choiceHandler, selectedRank):
   
   choiceHandler.finalcallback(choiceHandler.fullChoiceList[selectedRank])

def get_module_name(callback, view=None):
   """ Retrieve module name using a view. The view defaults to current active view. """
   name = helpers.get_module_from_view(view)
   callback(name)

def get_module_content(callback, view=None):
   """ Retrieve module content using a view. The view defaults to current active view. """
   source = helpers.get_view_content(view)
   callback(source)

def choose_scenario(callback, view=None):
   name = helpers.get_module_from_view(view)

   api = environment.getSwaggerAPI()
   fullChoiceList = api.ModuleDefAPI.ModuleDefAPI_Scenarios(name=name).result()
   
   lightChoiceList = []
   for item in fullChoiceList:
      lightChoiceList.append([item['label']])

   choiceHandler = input_handler.ChoiceInputHandler(finalcallback=callback, selectionDone=scenario_chosen, fullChoiceList=fullChoiceList, lightChoiceList=lightChoiceList)
   
   choiceHandler.choice_input()

def scenario_chosen(choiceHandler, selectedRank):
   choiceHandler.finalcallback(choiceHandler.fullChoiceList[selectedRank])