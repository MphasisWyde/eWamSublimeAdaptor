import sublime, sublime_plugin, os, sys, http.client, socket, json
from . import gold_helpers


class Bag1:
    data = -2
    def __init__(self):
        print(self.data)
        self.data = 0
    def add(self, x):
        self.data += x
        print(self.data)

class Bag2:
    bag1 = None
    def __init__(self):
        self.bag1 = Bag1()
    # def __dict__(self):
    #     pass
    def setBag1(self, bag1):
        self.bag1 = bag1

def todict(obj, classkey=None):
    if isinstance(obj, dict):
        data = {}
        for (k, v) in obj.items():
            data[k] = todict(v, classkey)
        return data
    elif hasattr(obj, "_ast"):
        return todict(obj._ast())
    elif hasattr(obj, "__iter__"):
        return [todict(v, classkey) for v in obj]
    elif hasattr(obj, "__dict__"):
        data = dict([(key, todict(value, classkey)) 
            for key, value in obj.__dict__.items()
            if not callable(value) and not key.startswith('_')])
        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    else:
        return obj

class GoldTestCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)
        
        bag_1 = Bag1()
        bag_1.add(5)

        bag_2 = Bag2()
        bag_2.setBag1(bag_1)

        # print(todict(bag_2))
        # print(json.dumps(bag_2.__dict__))
        # sublime.active_window().set_project_data(dict(bag_2))
        
        # sublime.active_window().show_input_panel("blabla1", "{example : sdf}, {truc2 : zep-ortu}", None, None, None)
        # sublime.active_window().show_input_panel("blabla2", "{example : sdf}, {truc2 : zep-ortu}", None, None, None)
        # sublime.active_window().show_input_panel("blabla3", "{example : sdf}, {truc2 : zep-ortu}", None, None, None)

        # sublime.active_window().active_view().set_name("d:\\desktop\\pouet.py")

        gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + type(self).__name__ + "." + sys._getframe().f_code.co_name)

    def is_enabled(self):
        return True
        # try:
        #     conn = http.client.HTTPConnection('localhost', 8082, timeout=0.1)
        #     conn.request("GET", "/aeWamManager/aModuleDef/aTest")
        #     resp = conn.getresponse()

        #     return True
        # except socket.timeout:
        #     sublime.status_message("*** WARNING: EWAM SERVICE UNREACHABLE ! ***")
        #     return False