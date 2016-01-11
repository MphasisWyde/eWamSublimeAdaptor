import sublime, sublime_plugin, ctypes, json, sys, http.client, socket
from . import gold_helpers, gold_environnement

class GoldPushEntityCommand(sublime_plugin.TextCommand):
   def run(self, edit):
      gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
      # Callback "open_class" when name has been entered

      gold_environnement.InitializeErrorList()
         
      self.view.erase_regions('errors')

      gold_environnement.goldErrorsView.set_read_only(False)
      gold_environnement.goldErrorsView.run_command("select_all")
      gold_environnement.goldErrorsView.run_command("right_delete")

      className = self.view.name().split('.')[0]
      print(className)
      source = self.view.substr(sublime.Region(0, self.view.size())).translate(str.maketrans( {'"': '\\\"' } ))
      
      
      conn = http.client.HTTPConnection('localhost:8082')
      conn.request("POST", "/aeWamManager/aModuleDef/"+className, source)
      resp = conn.getresponse()
      
      print(resp.status)

      if resp.status == 200:
         wholeRegion = sublime.Region(0, self.view.size())
         newText = resp.read().decode("ascii").replace('\r\n', '\n')
         self.view.replace(edit, wholeRegion, newText)
      else:
         lineRegions = self.view.split_by_newlines(sublime.Region(0, self.view.size()))
         errorList=json.loads(resp.read().decode("ascii").replace('\r\n', '\n'))
         
         

         errRegions = []
         for err in errorList:
            errRegions += [lineRegions[err['line']]]
            message = self.view.name() + ":" + str(err['line']) + ":" + str(err['offSet']) + ": " + err['msg'] + "\n"
            print(message)
            gold_environnement.goldErrorsView.run_command("insert", { 'characters' : message })

         self.view.add_regions('errors', errRegions, 'invalid', 'Packages/Gold/dot.png', sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE | sublime.DRAW_SQUIGGLY_UNDERLINE)

      gold_environnement.goldErrorsView.set_read_only(True)
      sublime.active_window().run_command("show_panel", { 'panel': 'output.golderrors' })

      conn.close()
         
        
   def is_enabled(self):
      try:
         className = self.view.name().split('.')[0]
         conn = http.client.HTTPConnection('localhost', 8082, timeout=0.1)
         conn.request("GET", "/aeWamManager/entitystatus/"+className)
         resp = conn.getresponse()
         parsed = json.loads(resp.read().decode("ascii").replace('\r\n', '\n'))

         return gold_helpers.IsGoldCode(self.view) and parsed['checkedOut']
      except socket.timeout:
         sublime.status_message("*** WARNING: EWAM SERVICE UNREACHABLE ! ***")
         return False




      