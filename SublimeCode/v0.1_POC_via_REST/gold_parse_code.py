import sublime, sublime_plugin, ctypes, json, sys, http.client
from . import *

class GoldParseCodeCommand(sublime_plugin.TextCommand):

   def run(self, edit, refresh):
      gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + sys._getframe().f_code.co_name)

      conn = http.client.HTTPSConnection('www.google.com')
      conn.request("GET", "/")
      resp = conn.getresponse()
      print(resp.status, resp.reason, resp.read())

      if refresh == None:
         refresh = True

      result = gold_environnement.Parse(self.view)

      self.view.erase_regions('errors')

      gold_environnement.goldErrorsView.set_read_only(False)
      gold_environnement.goldErrorsView.run_command("select_all")
      gold_environnement.goldErrorsView.run_command("right_delete")

      #if OK : set the new code
      if result['eWamReply']['myResult'] != "KO." and refresh:
         wholeRegion = sublime.Region(0, self.view.size())
         #print(wholeRegion)
         newText = result['eWamReply']['myResult'].replace('\r\n', '\n')
         #print(newText)
         self.view.replace(edit, wholeRegion, newText)
      #else retrieve error list
      else:
         lineRegions = self.view.split_by_newlines(sublime.Region(0, self.view.size()))

         errorList = result['eWamReply']['myErrors']

         errRegions = []
         for err in errorList:
            errRegions += [lineRegions[err['line']]]
            message = self.view.name() + ":" + str(err['line']) + ":" + str(err['offSet']) + ": " + err['msg'] + "\n"
            gold_environnement.goldErrorsView.run_command("insert", { 'characters' : message })

         self.view.add_regions('errors', errRegions, 'invalid', 'Packages/User/dot.png', sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE | sublime.DRAW_SQUIGGLY_UNDERLINE)
         #sublime.active_window().set_layout({ "cols": [0.0, 0.5, 1.0], "rows": [0.0, 0.33, 0.66, 1.0], "cells": [[0, 0, 1, 3], [1, 0, 2, 1], [1, 1, 2, 2], [1, 2, 2, 3]] })
         #self.view.erase_regions('blabla')

      gold_environnement.goldErrorsView.set_read_only(True)
      sublime.active_window().run_command("show_panel", { 'panel': 'output.golderrors' })

      gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + sys._getframe().f_code.co_name)

   def is_enabled(self):
      return gold_helpers.IsGoldCode(self.view) and gold_environnement.IsEnvironnementInitialized()