import sublime, sublime_plugin, sys, os, http.client, re, json
sys.path.append(os.path.join(os.path.dirname(__file__), "plugin"))
sys.path.append(os.path.join(os.path.dirname(__file__), "third-party"))
import environment

connection = None

def openHttpConnection():
   curEnv = environment.get_working_environment()
   if curEnv == None:
      sublime.error_message("eWAM environment not set. Please select your working environment.")
      return

   global connection
   url = curEnv['url']
   if url.find("http://") == 0:
      host = url[7:]
      connection = http.client.HTTPConnection(host)
   else:
      if url.find("https://") == 0:
         host = url[8:]
         connection = http.client.HTTPSConnection(host)

def httpRequest(method, path):
   openHttpConnection()
   print(method, path)
   connection.request(method, path)
   return connection.getresponse()


class WamGenericWindowCommandCommand(sublime_plugin.WindowCommand):

   # def is_enabled(self):
   #    return True

   # def is_visible(self):
   #    return True

   # def description(self):
   #    return "Description"

   def run(self, method, path, params, action):

      expandedPath = ExpandPath(path)

      response = httpRequest(method, expandedPath)
      if action == None or action == '':
         return

      self.window.active_view().run_command(action, { "jsonData": json.loads(response.read().decode('utf-8')) } )
      # { "text": response.read().decode('ascii') }

      # if action not in globals():
      #    message = "Method '" + action + "' couldn't be found. [" + __name__ + " : " + type(self).__name__ + "." + sys._getframe().f_code.co_name + "]"
      #    print("Gold Plugin Error: " + message)
      #    sublime.error_message(message)
      #    return


      # actionClass = globals()[action]
      # if actionClass != None:
      #    actionCall = actionClass()
      #    actionCall.run(response)


class WamGenericContextualCommandCommand(sublime_plugin.TextCommand):

   # def is_enabled(self):
   #    return True

   # def is_visible(self):
   #    return True

   # def description(self):
   #    return "Open en eWAM environment in a new workspace"

   def want_event(self):
        True

   def run(self, edit, event):
      pass

def wam_input_entity_name():
   return "aRedgisTest"


class WamOpenInNewWindowCommand(sublime_plugin.TextCommand):

   def run(self, edit, jsonData):
      newView = sublime.active_window().new_file()
      # newView.set_name()
      # newView.set_scratch(True)

      # parsed = json.loads(resp.read().decode("ascii").replace('\r\n', '\n'))

      newView.insert(edit, 0, jsonData['content'].replace('\r\n', '\n'))
      # newView.set_syntax_file('Packages/Gold/gold.tmLanguage')


def ExpandTag(tag):
   methodName = tag.strip("{}")
   if methodName not in globals():
      message = "Ignoring token {" + methodName + "} : method '" + methodName + "' couldn't be found. [" + __name__ + " : " + sys._getframe().f_code.co_name + "]"
      print("Gold Plugin Error: " + message)
      sublime.error_message(message)
      result = tag

   else:
      method = globals()[methodName]
      result = method()

   return result

def ExpandPath(path):
   newPath = ""

   identifierRegex = re.compile(r"\{[a-zA-Z0-9_]+\}")

   start = 0

   match = identifierRegex.search(path)
   while match != None:

      methodName = path[start+match.start():start+match.end()].strip("{}")
      if methodName not in globals():
         message = "Ignoring token {" + methodName + "} : method '" + methodName + "' couldn't be found. [" + __name__ + " : " + sys._getframe().f_code.co_name + "]"
         print("Gold Plugin Error: " + message)
         sublime.error_message(message)
         newPath = newPath + path[start:start+match.end()]
         
      else:
         identMethod = globals()[methodName]
         replacement = identMethod()
         newPath = newPath + path[start:start+match.start()] + replacement

      start = start+match.end()
      match = identifierRegex.search(path[start:])

   newPath = newPath + path[start:]

   return newPath


class WamSwaggerOpenClassCommand(sublime_plugin.WindowCommand):

   def is_enabled(self):
      return True

   def is_visible(self):
      return True

   def description(self):
      return "Open class using Swagger API"

   def run(self):
      api = environment.getSwaggerAPI()
      print("Swag! ", api)
      # res = api.ModuleDefAPI.classOrModule(name="aRedgisTest").result()
      # print(res)
      # api.get_model('classOrModule')
      # api.get_model('ModuleDefAPI')

      print("descendants: ", api.ModuleDefAPI.ModuleDefAPI_GetDescendants(name="aFullObject").result())

      print("Get: ", api.ModuleDefAPI.ModuleDefAPI_Get(name="aRedgisTest").result())

      print("api", locals()['api'])

      moduleAPI = getattr(locals()['api'], 'ModuleDefAPI')
      print("attr:", moduleAPI)

      method = getattr(moduleAPI, 'ModuleDefAPI_Get')
      print(method)

      kwargs = {'name': "aRedgisTest"}
      print(method(**kwargs).result())

