import sublime
import sublime_plugin
import subprocess
'''
import threading
import webbrowser
import os
'''

class OpenUrlCommand(sublime_plugin.TextCommand):
    def run(self, edit, url=None):
        subprocess.call('start '+url, shell=True)

'''
class OpenUrlCommand(sublime_plugin.TextCommand):
    def run(self, edit, filename=None):
        th = URLThread(filename)
        th.start()

class URLThread(threading.Thread):
    def __init__(self, filename=None):
        self.filename = filename
        threading.Thread.__init__(self)

    def run(self):
        if self.filename is not None:
            #subprocess.run(["dir"])
            #subprocess.call('start C:/Users/Kika/Desktop/test/test.bat', shell=True)

            #webbrowser.open(self.filename)
            #os.system('start C:/Users/Desktop/test/test.bat')
            #subprocess.call("notepad.exe %s" % self.filename)
            filepath="C:/Users/Kika/Desktop/test/test.bat"
            p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)

            stdout, stderr = p.communicate()
            #print p.returncode # is 0 if success

'''