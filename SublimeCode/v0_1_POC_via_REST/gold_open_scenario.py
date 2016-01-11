import sublime, sublime_plugin, ctypes, json, sys, http.client


class GoldOpenScenarioCommand(sublime_plugin.TextCommand):

   def log_panel_done(self, picked):
        if 0 > picked < len(self.results):
            return
        item = self.results[picked]
        conn = http.client.HTTPConnection('localhost:8082')
        conn.request('GET', '/aeWamManager/scenario/'+item)
        resp = conn.getresponse()
        conn.close()

   def run(self, edit, command, method="GET"):
      className = self.view.name().split('.')[0]   
      conn = http.client.HTTPConnection('localhost:8082')
      conn.request(method, command + '/'+className)
      resp = conn.getresponse()

      self.results = json.loads(resp.read().decode("ascii").replace('\r\n', '\n'))
      window = sublime.active_window()
      window.show_quick_panel(self.results, self.log_panel_done, sublime.MONOSPACE_FONT)
      
      conn.close()
