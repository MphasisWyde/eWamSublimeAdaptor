import sublime, sublime_plugin, ctypes, json, sys, http.client
from . import gold_helpers

class GoldGotoDefinitionCommand(sublime_plugin.TextCommand):
   
   # def __init__(self, XXXX):
   #    pass
   #    self.result = None

   def run(self, edit, event):
      gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
      
      x = int(event["x"])
      y = int(event["y"])

      selectedWord = self.view.word( self.view.window_to_text((x, y)) )
      searchName = self.view.substr(selectedWord)

      conn = http.client.HTTPConnection('localhost:8082')
      conn.request("GET", "/aeWamManager/searchEntities/"+searchName)
      resp = conn.getresponse()
      self.results = json.loads(resp.read().decode("ascii").replace('\r\n', '\n'))

      if len(self.results) > 1:
         window = sublime.active_window()
         window.show_quick_panel(self.results, self.entity_chosen, sublime.MONOSPACE_FONT)
      else:
         self.view.run_command("gold_do_open_class", {"className": self.results[0]})

      conn.close()

      gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)

   def is_enabled(self):
      return gold_helpers.IsGoldCode(self.view)

   def want_event(self):
      return True

   def entity_chosen(self, picked):
        if picked == -1 or picked > len(self.results):
            return
        item = self.results[picked]
        self.view.run_command("gold_do_open_class", {"className": item})
        print(item)