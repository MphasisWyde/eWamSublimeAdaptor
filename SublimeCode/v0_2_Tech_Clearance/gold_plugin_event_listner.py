import sublime, sublime_plugin, ctypes, sys
from . import gold_helpers

class GoldPluginEventListner(sublime_plugin.EventListener):
   # def on_new(self, view):
   #    gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    None

   # def on_new_async(self, view):
   #    gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    None

   # def on_clone(self, view):
   #    gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    None

   # def on_clone_async(self, view):
   #    gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    None

   # def on_load(self, view):
   #    gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + " " + view.file_name())
   #    gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + " " + view.file_name())
   #    None

   # def on_load_async(self, view):
   #    gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + " " + view.file_name())
   #    gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + " " + view.file_name())
   #    None 

   def on_pre_close(self, view):
      gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
      sublime.ok_cancel_dialog("want to save to eWAM before closing ?")
      gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
      None

   # def on_close(self, view):
   #    gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    None 

   # def on_pre_save(self, view):
   #    gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    None

   # def on_pre_save_async(self, view):
   #    gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    None

   # def on_post_save(self, view):
   #    gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    None

   # def on_post_save_async(self, view):
   #    gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    None

   # def on_modified(self, view):
   #    gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_modified_async(self, view):
   #    gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_selection_modified(self, view):
   #    gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_selection_modified_async(self, view):
   #    gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_activated(self, view):
   #    gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_activated_async(self, view):
   #    gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_deactivated(self, view):
   #    gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_deactivated_async(self, view): 
   #    gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_text_command(self, view, command_name, args):
   #    gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + " " + command_name + " " + str(args))
   #    gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + " " + command_name)
   #    return None #(new_command_name, new_args)

   def on_window_command(self, window, command_name, args):
      gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + " " + command_name)
      sublime.message_dialog("sdf")
      gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + " " + command_name)
      return None #(new_command_name, new_args)

   # def post_text_command(self, view, command_name, args):
   #    gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + " " + command_name)
   #    gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + " " + command_name)
   #    None

   # def post_window_command(self, window, command_name, args):
   #    gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + " " + command_name)
   #    gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + " " + command_name)
   #    None

   # def on_query_context(self, view, key, operator, operand, match_all):
   #    gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    None

   # def on_query_completions(self, view, prefix, locations):
   #    gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + " " + prefix + " " + locations)
   #    gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    None
   
   None
