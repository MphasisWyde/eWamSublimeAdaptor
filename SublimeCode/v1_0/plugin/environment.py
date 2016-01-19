import sublime, uuid


def get_environments():
   settings = sublime.load_settings("wam.sublime-settings")
   if settings == None:
      return []

   env_list = settings.get("environments")
   if env_list == None:
      env_list = []

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
   if not 'wam' in prj_data:
      prj_data['wam'] = {}

   selected_env = get_environment_by_index(index)
   prj_data['wam']['wam_working_environment'] = selected_env['name']

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


def get_working_environment():
   wnd = sublime.active_window()
   prj_data = wnd.project_data()
   selected_name = prj_data['wam']['wam_working_environment']
   if selected_name == None:
      return None

   working_env = get_environment_by_name(selected_name)

   if working_env == None:
      reset_working_environment()

   return working_env
