import sublime, sublime_plugin, ctypes, json, sys, http.client
from . import *

class GoldGenericCommandCommand(sublime_plugin.TextCommand):

   def run(self, edit, command, method="GET"):
      className = self.view.name().split('.')[0]   
      conn = http.client.HTTPConnection('localhost:8082')
      conn.request(method, command)
      resp = conn.getresponse()

      newView = sublime.active_window().new_file()
      newView.set_name(command)
      newView.set_scratch(True)

      parsed = json.loads(resp.read().decode("ascii").replace('\r\n', '\n'))
      newView.insert(edit, 0, json.dumps(parsed, indent=4, sort_keys=True))
      newView.set_syntax_file('Packages/User/gold.tmLanguage')
      
      conn.close()
   