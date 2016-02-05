import sublime

class InputHandler:
   finalcallback = None
   useListSelection = False
   lightChoiceList = [] # For quick panel display
   fullChoiceList = [] # To retireve the full information after quick panel selection
   getChoiceList = None
   inputDone = None # Called once the user input is done, to retrieve what the final callback should get in parameter
   skipChoiceListIfOneItem = False

   def __init__(self, finalcallback, useListSelection, getChoiceList, inputDone, skipChoiceListIfOneItem=False):
      self.finalcallback = finalcallback
      self.useListSelection = useListSelection
      self.getChoiceList = getChoiceList
      self.skipChoiceListIfOneItem = skipChoiceListIfOneItem
      self.inputDone = inputDone

   def input_text(self, label, preset):
      sublime.active_window().show_input_panel(label, preset, self.fill_choicelists, None, self.on_input_canceled)

   def fill_choicelists(self, text):
      self.text = text

      if self.useListSelection:
         choices = self.getChoiceList(self.text)
         self.fullChoiceList = choices[0]
         self.lightChoiceList = choices[1]
         self.choice_input()

   def choice_input(self):
      if self.skipChoiceListIfOneItem and len(fullChoiceList) == 1:
         self.inputDone(fullChoiceList[0], self.finalcallback)
         return
      self.choice_list(self.lightChoiceList, self.on_selection_done, 0, 0, None)

   def choice_list(self, choiceList, selected_callback, flags=0, selected_index=0, on_highlighed=None):
      sublime.active_window().show_quick_panel(choiceList, selected_callback, flags, selected_index, on_highlighed)

   def on_input_canceled(self):
      pass

   def on_selection_done(self, selected_rank):
      self.inputDone(self.fullChoiceList[selected_rank], self.finalcallback)


