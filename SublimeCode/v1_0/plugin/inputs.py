import sublime
import environment
import helpers
import input_handler


""" Class name retrieving from user input
"""
def get_classname(callback, view=None):
   inputHandler = input_handler.InputHandler(finalcallback=callback, useListSelection=True, getChoiceList=on_classnameinput_done, inputDone=on_classnameinput_completed, skipChoiceListIfOneItem=False)
   inputHandler.input_text("Enter class name:", "")

def on_classnameinput_done(text):
   api = environment.getSwaggerAPI()

   choices = [[], []]
   choices[0] = api.MMBrowserAPI.MMBrowserAPI_searchEntities(q=text, _class="true").result()

   for item in choices[0]:
      choices[1].append([item.name + " : " + item.theType, item.location])

   return choices

def on_classnameinput_completed(itemSelected, callback):
   callback(itemSelected.name)

# End of class name retrieval

def searchEntity(callback, name):
   inputHandler = input_handler.InputHandler(finalcallback=callback, useListSelection=True, getChoiceList=None, inputDone=entityChosen, skipChoiceListIfOneItem=False)
   api = environment.getSwaggerAPI()

   choices = [[], []]
   choices[0] = api.MMBrowserAPI.MMBrowserAPI_searchEntities(q=name).result()

   for item in choices[0]:
      # print(item)
      # if item.ownerName == "":
      #    choices[1].append([item.name + " : " + item.theType, item.location])
      # else:
      # choices[1].append([item[name] + " : " + item.theType, item.location])
      choices[1].append([item['name'] + " : " + item['theType'], item['location']])

   inputHandler.fullChoiceList = choices[0]
   inputHandler.lightChoiceList = choices[1]

   inputHandler.choice_input()

def entityChosen(selected_entity, callback):
   callback(selected_entity)
   # selected_entity.ownerName

def get_module_name(callback, view=None):
   """ Retrieve module name using a view. The view defaults to current active view. """
   name = helpers.get_module_from_view(view)
   callback(name)

def get_module_content(callback, view=None):
   """ Retrieve module content using a view. The view defaults to current active view. """
   source = helpers.get_view_content(view)
   callback(source)

