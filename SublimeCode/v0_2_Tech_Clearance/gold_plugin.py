import sys, os, sublime
sys.path.append(os.path.join(os.path.dirname(__file__), "third-party"))
from bravado.client import SwaggerClient



def plugin_loaded():
   for wnd in sublime.windows():
      print(wnd.id())

def plugin_unloaded():
   sublime.ok_cancel_dialog("hello")
   pass


""" Represents a workspace project composed of an eWAM environment and a set of editable entities opened in this workspace
"""
class Project:
   
   """ eWAM environment associated with this project
   """
   environment = None

   def __init__(self):
      pass

   def new(self, env):
      environment = env

   def restore(self, env):
      # what is there to do here ?
      pass




""" Represents an eWAM environment (reachable via REST API)
"""
class Environment:

   uniq_name = ""
   base_url = ""
   api = None
   
   """ Edits currently opened in project
   """
   edits = []

   def __init__(self, url, name):
      self.base_url = url
      self.uniq_name = name
      self.UpdateAPIMapping(self)

   def UpdateAPIMapping(self, swagger_path="/swagger/swagger.json"):
      api = SwaggerClient.from_url(base_url + swagger_path)

      #self.api = SwaggerClient(base_url + swagger_path, http_client=http_client)



""" Represents an editable entity (class, module, scenarios, Produce C++, CPP Project, Bundle, ... anything)
"""
class Edit:

   name = ""
   uri = ""
   project = None
   environment = None

   def __init__(self, name, uri, view, environment):
      self.name = name
      self.uri = uri
      self.view = view
      self.project = project
      self.env = environment

   def load():
      None

   def checkout():
      None

   def checkin():
      None

   def check():
      None

   def push():
      None

   def status():
      None

   def close():
      None

