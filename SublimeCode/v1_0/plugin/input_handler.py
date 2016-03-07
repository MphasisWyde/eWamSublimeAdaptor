import sublime

class TextInputHandler:
   finalcallback = None
   inputDone = None # Called once the user input is done, to retrieve what the final callback should get in parameter

   def __init__(self, finalcallback, inputDone):
      self.finalcallback = finalcallback
      self.inputDone = inputDone

   def input_text(self, label, preset=""):
      sublime.active_window().show_input_panel(label, preset, self.on_input_done, None, self.on_input_canceled)

   def on_input_done(self, text):
      self.inputDone(self, text)

   def on_input_canceled(self):
      pass


class ChoiceInputHandler:
   finalcallback = None
   lightChoiceList = [] # For quick panel display
   fullChoiceList = [] # To retireve the full information after quick panel selection
   skipChoiceListIfOneItem = True
   preselectedItem = 0
   selectionDone = None # Cal<led once the user input is done, to retrieve what the final callback should get in parameter
   

   def __init__(self, finalcallback, selectionDone, fullChoiceList, lightChoiceList):
      self.finalcallback = finalcallback
      self.fullChoiceList = fullChoiceList
      self.lightChoiceList = lightChoiceList
      self.skipChoiceListIfOneItem = True
      self.preselectedItem = 0
      self.selectionDone = selectionDone

   def choice_input(self):
      if self.skipChoiceListIfOneItem and len(self.fullChoiceList) == 1:
         self.selectionDone(self, 0)
         return
      else:
         sublime.active_window().show_quick_panel(self.lightChoiceList, self.on_selection_done, 0, self.preselectedItem, self.on_item_highlighted)     

   def on_selection_done(self, selected_rank):
      if selected_rank == -1:
         self.on_selection_canceled
         return

      self.selectionDone(self, selected_rank)

   def on_item_highlighted(self, hl_rank):
      pass

   def on_selection_canceled(self):
      pass
