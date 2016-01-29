import sublime, time

def update_current_view_content(data):
   print(data)


def open_gold_window(name, content):
   newView = sublime.active_window().new_file()

   while newView.is_loading():
      time.sleep(0.1)

   newView.set_scratch(True)
   newView.set_name(name + ".gold")
   sublime.set_clipboard( content.replace('\r\n', '\n') )
   newView.run_command("paste")

   newView.set_syntax_file('Packages/Gold/gold.tmLanguage')