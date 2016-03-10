import sublime, sublime_plugin, ctypes, json, sys, http.client

class GoldGitLogCommand(sublime_plugin.TextCommand):
    def run(self, edit=None):
        #fn = self.get_file_name()
        return self.run_log(self, '--', '')

    def log_panel_done(self, picked):
        if 0 > picked < len(self.results):
            return
        item = self.results[picked]
        self.view.run_command("gold_do_open_class", {"className": item})
        print(item)

    def run_log(self, follow, *args):
        conn = http.client.HTTPConnection('localhost:8082')
        conn.request("GET", "/aeWamManager/searchEntities/awt")
        resp = conn.getresponse()
        self.results = json.loads(resp.read().decode("ascii").replace('\r\n', '\n'))
       
        window = sublime.active_window()
        window.show_quick_panel(self.results, self.log_panel_done, sublime.MONOSPACE_FONT)

    