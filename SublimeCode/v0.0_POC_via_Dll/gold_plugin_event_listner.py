import sublime, sublime_plugin, ctypes, User.gold_helpers, sys, string

class GoldPluginEventListner(sublime_plugin.EventListener):
   # def on_new(self, view):
   #    User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_new_async(self, view):
   #    User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_clone(self, view):
   #    User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_clone_async(self, view):
   #    User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_load(self, view):
   #    User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + view.file_name())
   #    User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + view.file_name())
   #    return None

   # def on_load_async(self, view):
   #    User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + view.file_name())
   #    User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + view.file_name())
   #    return None

   # def on_pre_close(self, view):
   #    User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_close(self, view):
   #    User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_pre_save(self, view):
   #    User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_pre_save_async(self, view):
   #    User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_post_save(self, view):
   #    User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_post_save_async(self, view):
   #    User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_modified(self, view):
   #    User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)

   #    regions = view.get_regions('errors')
   #    print(regions[0])

   #    User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   def on_modified_async(self, view):
      User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)

      if User.gold_helpers.IsGoldCode(view):
         view.run_command("gold_parse_code", {"refresh": False})

      User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
      return None

   # def on_selection_modified(self, view):
   #    User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_selection_modified_async(self, view):
   #    User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_activated(self, view):
   #    User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_activated_async(self, view):
   #    User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_deactivated(self, view):
   #    User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_deactivated_async(self, view): 
   #    User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   def on_text_command(self, view, command_name, args):
      User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + " " + command_name + " " + str(args))

      if args == None or not 'event' in args:
         return None

      evt = args['event']

      if view == User.gold_environnement.goldErrorsView and evt['button'] == 1:
         pt = view.window_to_text((evt["x"], evt["y"]))
         lineReg = view.line(pt)
         line = view.substr(lineReg)
         tokens = str.split(line, ':')

         if lineReg.empty():
            return None

         #Put focus on view with name "tokens[0]"
         wnd = view.window()
         allViews = wnd.views()
         for tmpView in allViews:
            if tmpView.name() == tokens[0]:
               break

         #Put focus on lin "tokens[1]"
         lineRegions = tmpView.split_by_newlines(sublime.Region(0, tmpView.size()))
         tmpView.sel().clear()
         selRegion = lineRegions[int(tokens[1])]
         tmpView.sel().add(selRegion)

         wnd.focus_view(tmpView)
         tmpView.show_at_center(selRegion)

      User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + " " + command_name)
      return None #(new_command_name, new_args)

   # def on_window_command(self, window, command_name, args):
   #    User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + " " + command_name)
   #    User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + " " + command_name)
   #    return None #(new_command_name, new_args)

   # def post_text_command(self, view, command_name, args):
   #    User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + " " + command_name)
   #    User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + " " + command_name)
   #    None

   # def post_window_command(self, window, command_name, args):
   #    User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + " " + command_name)
   #    User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + " " + command_name)
   #    None

   # def on_query_context(self, view, key, operator, operand, match_all):
   #    User.gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    User.gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    None

   # None
   