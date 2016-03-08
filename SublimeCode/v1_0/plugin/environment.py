import sublime, uuid
from bravado.client import SwaggerClient

swaggerClient = None


def get_environments():
   settings = sublime.load_settings("wam.sublime-settings")
   if settings == None:
      return dict([])

   env_list = settings.get("environments")
   if env_list == None:
      env_list = dict([])

   return env_list


def get_environment_by_index(index):
   envs = get_environments()
   for i, item in enumerate(envs):
      if i == index:
         return envs[item]
   return None


def get_environment_by_name(name):
   envs = get_environments()
   if name in envs:
      return envs[name]
   else:
      return None


def save_environment(name, url):
   env_list = get_environments()
   env_uuid =  str( uuid.uuid3(uuid.NAMESPACE_URL, url+"/"+name) )
   
   env_list[name] = { 'name': name, "url": url, "uuid": env_uuid }
      
   settings = sublime.load_settings("wam.sublime-settings")
   settings.set("environments", env_list)
   sublime.save_settings("wam.sublime-settings")


def clear_environments():
   settings = sublime.load_settings("wam.sublime-settings")
   if settings == None:
      return

   env_list = {}
   setClientAPIFromEnv(None)
   settings.set("environments", env_list)
   sublime.save_settings("wam.sublime-settings")   


def select_environment(window, action):
   envs = get_environments()

   working_env = get_working_environment()
   if working_env == None:
      working_name = ''
   else:
      working_name = working_env['name']

   selected_item = -1

   items = []
   for i, env in enumerate(envs):
      if envs[env]['name'] == working_name:
         selected_item = i
      items.append([envs[env]['name'], envs[env]['url']])
      # [["Wynsure 5.6", "http://localhost:8082"], ["Wynsure 5.5", "http://localhost:8083"]]

   window.show_quick_panel(items, action, 0, selected_item, None)


def set_working_environment(index):
   if index == -1:
      return

   wnd = sublime.active_window()
   prj_data = wnd.project_data()
   if prj_data == None:
      prj_data = {}

   if not 'wam' in prj_data:
      prj_data['wam'] = {}

   selected_env = get_environment_by_index(index)
   prj_data['wam']['wam_working_environment'] = selected_env['name']
   setClientAPIFromEnv(selected_env)

   wnd.set_project_data(prj_data)


def remove_environment(index):
   if index == -1:
      return

   selected_env = get_environment_by_index(index)

   wnd = sublime.active_window()
   prj_data = wnd.project_data()
   if 'wam' in prj_data:
      if 'wam_working_environment' in prj_data['wam']:
         if prj_data['wam']['wam_working_environment'] == selected_env['name']:
            prj_data['wam']['wam_working_environment'] = ''
            setClientAPIFromEnv(None)
            wnd.set_project_data(prj_data)

   settings = sublime.load_settings("wam.sublime-settings")
   envs = settings.get("environments")
   del envs[selected_env['name']]
   settings.set("environments", envs)
   sublime.save_settings("wam.sublime-settings")


def reset_working_environment():
   wnd = sublime.active_window()
   prj_data = wnd.project_data()
   if not 'wam' in prj_data:
      prj_data['wam'] = {}

   prj_data['wam']['wam_working_environment'] = ''
   setClientAPIFromEnv(None)


def get_working_environment():
   wnd = sublime.active_window()
   prj_data = wnd.project_data()
   if prj_data == None:
      return None

   if 'wam' in prj_data:
      if 'wam_working_environment' in prj_data['wam']:
         selected_name = prj_data['wam']['wam_working_environment']
   if selected_name == None:
      return None

   working_env = get_environment_by_name(selected_name)

   if working_env == None:
      reset_working_environment()

   return working_env


def setClientAPIFromEnv(env):
   global swaggerClient
   if env == None:
      swaggerClient = None
   else:
      print("Initializing SwaggerClient with " + env['url'] + "/api/rest/documentation")

      config = {
          # === bravado config ===

          # Determines what is returned by the service call.
          'also_return_response': False,

          # === bravado-core config ====

          #  validate incoming responses
          'validate_responses': False,

          # validate outgoing requests
          'validate_requests': False,

          # validate the swagger spec
          'validate_swagger_spec': False,

          # Use models (Python classes) instead of dicts for #/definitions/{models}
          'use_models': False,

          # # List of user-defined formats
          # 'formats': [my_super_duper_format],
      }

      swagger_url = env['url'] + "/api/rest/documentation"

      swaggerClient = SwaggerClient.from_url(swagger_url, config=config)

   if swaggerClient == None:
      sublime.error_message("Swagger API couldn't be loaded from environment " + env['name'] + ": " + swagger_url)


def getSwaggerAPI():
   global swaggerClient
   if swaggerClient == None:
      setClientAPIFromEnv(get_working_environment())

   return swaggerClient
