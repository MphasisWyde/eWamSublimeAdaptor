import sublime, sublime_plugin
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "plugin"))
sys.path.append(os.path.join(os.path.dirname(__file__), "third-party"))

import helpers
import environment
import actions
import inputs


class WamInsertTextCommand(sublime_plugin.TextCommand):

   def is_enabled(self):
      return True

   def is_visible(self):
      return True

   def description(self):
      return "Insert text in a buffer..."

   def want_event(self):
      False

   def run(self, edit, text):
      self.view.insert(edit, 0, text)


class WamAppendTextCommand(sublime_plugin.TextCommand):

   def is_enabled(self):
      return True

   def is_visible(self):
      return True

   def description(self):
      return "Append text in a buffer..."

   def want_event(self):
      False

   def run(self, edit, text):
      self.view.insert(edit, self.view.size(), text)


class WamClearTextCommand(sublime_plugin.TextCommand):

   def is_enabled(self):
      return True

   def is_visible(self):
      return True

   def description(self):
      return "Clear text in a buffer..."

   def want_event(self):
      False

   def run(self, edit):
      readonly = False

      if self.view.is_read_only():
         readonly = True
         self.view.set_read_only(False)

      self.view.erase(edit, sublime.Region(0, self.view.size()))

      if readonly:
         self.view.set_read_only(True)


class WamReplaceTextCommand(sublime_plugin.TextCommand):

   def is_enabled(self):
      return True

   def is_visible(self):
      return True

   def description(self):
      return "Clear text in a buffer..."

   def want_event(self):
      False

   def run(self, edit, text):
      self.view.replace(edit, sublime.Region(0, self.view.size()), text)


class WamGotoDefinitionCommand(sublime_plugin.TextCommand):
   word = None
   x = -1
   y = -1
   
   def is_enabled(self):
      return helpers.is_a_gold_view(self.view)

   def is_visible(self):
      return helpers.is_a_gold_view(self.view)

   def description(self):
      return "Goto definition"

   def want_event(self):
      return True

   def run(self, edit, event):
      self.x = int(event["x"])
      self.y = int(event["y"])

      self.word = helpers.get_word_at(self.x, self.y, self.view)
      if self.word == None or self.word == "":
         return

      inputs.searchEntity(self.inputCallback, self.word)

   def inputCallback(self, entity):
      actions.open_entity(entity['label'], entity)

class WamGotoDefinitionFromKeyCommand(sublime_plugin.WindowCommand):
   word = None

   def is_enabled(self):
      return helpers.is_a_gold_view(sublime.active_window().active_view())

   def is_visible(self):
      return helpers.is_a_gold_view(sublime.active_window().active_view())

   def description(self):
      return "Goto definition"

   def run(self):
      view = sublime.active_window().active_view()

      selection = view.sel()
      self.word = view.substr(view.word(selection[0]))

      if self.word == None or self.word == "":
         return

      inputs.searchEntity(self.inputCallback, self.word)

   def inputCallback(self, entity):
      actions.open_entity(entity['label'], entity)
