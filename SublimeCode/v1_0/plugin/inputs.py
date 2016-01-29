import sublime
import environment


class InputHandler:
   finalcallback = None
   textInput = False
   text = ""
   inputTextCallback = None
   useListSelection = False
   choiceList = ()

   def __init__(self, finalcallback, textInput, useListSelection, getChoiceList):
      self.finalcallback = finalcallback
      self.textInput = textInput
      self.inputTextCallback = inputTextCallback
      self.useListSelection = useListSelection

   def input_text(self, label, preset):
      sublime.active_window().show_input_panel(label, preset, self.on_input_done, None, self.on_input_canceled)

   def on_input_done(self, text):
      self.text = text
      if self.useListSelection:
         choiceList = getChoiceList(self.text)


   def on_input_canceled(self):
      pass

   def on_selection_done(self, selectionRank):
      pass


def get_classname(callback):
   inputHandler = InputHandler(callback, True, on_classinput_done,True)
   inputHandler.inputText("Enter class name:", "")


def on_classinput_done(text, callback):
   api = environment.getSwaggerAPI()
   print(api.MMBrowserAPI.MMBrowserAPI_searchEntities(q=text, _class=True).result())

def get_current_view_content(callback):
   callback()
