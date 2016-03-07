import sublime, sublime_plugin
import sys, os, time

sys.path.append(os.path.join(os.path.dirname(__file__), "plugin"))
sys.path.append(os.path.join(os.path.dirname(__file__), "third-party"))

import helpers
import environment
import actions
import inputs


class WamEventListener(sublime_plugin.EventListener):
   # def on_new(self, view):
   #    helpers.log_info("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    helpers.log_info("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_new_async(self, view):
   #    helpers.log_info("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    helpers.log_info("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_clone(self, view):
   #    helpers.log_info("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    helpers.log_info("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_clone_async(self, view):
   #    helpers.log_info("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    helpers.log_info("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_load(self, view):
   #    helpers.log_info("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + view.file_name())
   #    helpers.log_info("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + view.file_name())
   #    return None

   # def on_load_async(self, view):
   #    helpers.log_info("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + view.file_name())
   #    helpers.log_info("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + view.file_name())
   #    return None

   # def on_pre_close(self, view):
   #    helpers.log_info("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    helpers.log_info("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_close(self, view):
   #    helpers.log_info("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    helpers.log_info("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_pre_save(self, view):
   #    helpers.log_info("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    helpers.log_info("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_pre_save_async(self, view):
   #    helpers.log_info("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    helpers.log_info("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_post_save(self, view):
   #    helpers.log_info("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    helpers.log_info("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_post_save_async(self, view):
   #    helpers.log_info("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    helpers.log_info("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_modified(self, view):
   #    helpers.log_info("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)

   #    regions = view.get_regions('errors')
   #    print(regions[0])

   #    helpers.log_info("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   view_to_parse = None

   def on_modified_async(self, view):
      helpers.log_info("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
      return
      now = time.time()

      if self.view_to_parse == None and helpers.is_a_gold_view(self.view_to_parse):
         self.view_to_parse = view
         name = helpers.get_module_from_view(self.view_to_parse)
         if helpers.is_entity_checkedout(name):
            sublime.set_timeout_async(self.treat_parses, 5000)

      helpers.log_info("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
      return None

   def treat_parses(self):
      if self.view_to_parse != None:
         print("parse")
         self.view_to_parse.run_command("wam_parse", {"refresh": False})
         self.view_to_parse = None

   # def on_selection_modified(self, view):
   #    helpers.log_info("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    helpers.log_info("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_selection_modified_async(self, view):
   #    helpers.log_info("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    helpers.log_info("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   def on_activated(self, view):
      helpers.log_info("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)

      actions.update_readonly(view)

      helpers.log_info("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
      return None

   def on_activated_async(self, view):
      helpers.log_info("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)

      actions.update_readonly(view)

      helpers.log_info("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)

      return None

   # def on_deactivated(self, view):
   #    helpers.log_info("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    helpers.log_info("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   # def on_deactivated_async(self, view): 
   #    helpers.log_info("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    helpers.log_info("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    return None

   def on_text_command(self, view, command_name, args):
      helpers.log_info("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + " " + command_name + " " + str(args))

      if args == None or not 'event' in args:
         return None

      evt = args['event']

      errorView = view.window().find_output_panel('gold_error_panel')

      if errorView == view and evt['button'] == 1:
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

      helpers.log_info("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + " " + command_name)
      return None #(new_command_name, new_args)

   # def on_window_command(self, window, command_name, args):
   #    helpers.log_info("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + " " + command_name)
   #    helpers.log_info("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + " " + command_name)
   #    return None #(new_command_name, new_args)

   # def post_text_command(self, view, command_name, args):
   #    helpers.log_info("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + " " + command_name)
   #    helpers.log_info("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + " " + command_name)
   #    None

   # def post_window_command(self, window, command_name, args):
   #    helpers.log_info("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + " " + command_name)
   #    helpers.log_info("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name + " " + command_name)

   # def on_query_context(self, view, key, operator, operand, match_all):
   #    helpers.log_info("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   #    helpers.log_info("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)

   def on_query_completions(self, view, prefix, locations):
      # helpers.log_info("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   
      # if (not helpers.is_a_gold_view(view)) or (len(prefix) < 4):
      #    return []
   
      # api = environment.getSwaggerAPI()
   
      # fullChoiceList = api.MMBrowserAPI.MMBrowserAPI_searchEntities(q=prefix).result()
   
      # result = []
      # for item in fullChoiceList:
      #    result.append((item['label'], item['label']))

      # print(result)

      # helpers.log_info("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)

      # return result

      helpers.log_info("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
   
      if not helpers.is_a_gold_view(view):
         return []

      moduleName = helpers.get_module_from_view(view)
      sourceCode = helpers.get_view_content(view).replace('\n', "\\r\\n")
      
      api = environment.getSwaggerAPI()
      tSuggestBody = api.get_model("tSuggestBody")
      tImplem = api.get_model("tImplem")

      rowcol = view.rowcol(locations[0])
      lineRegion = view.line(locations[0])
      lineContent = view.substr(lineRegion)
      lineInfo = { "lineContent": lineContent, "lineNumber": rowcol[0]+1, "ColumnNumber": rowcol[1]+1 }

      implem = { "name": moduleName, "ancestor": "", "content": sourceCode }

      suggestBody = tSuggestBody(implem=implem, lineInfo=lineInfo)

      fullChoiceList = api.ModuleDefAPI.ModuleDefAPI_Suggest(name=moduleName, body=suggestBody).result()

      result = []
      for item in fullChoiceList["items"]:
         if item['inserText'] == "":
            result.append((item["label"], item["label"]))
         else:
            result.append((item["label"], item["insertText"]))

      helpers.log_info("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)

      if result == []:
         flag = 0
      else:
         flag = sublime.INHIBIT_WORD_COMPLETIONS

      return (result, flag)

   # None
   