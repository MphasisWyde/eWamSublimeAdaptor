import sublime, ctypes, sys, json
from . import gold_helpers, gold_globals

def IsEnvironnementInitialized():
    if gold_globals.hWamAPI == None:
        return False

    projName = sublime.active_window().project_file_name()
    if projName == None:
        return False

    projData = sublime.active_window().project_data()
    if projData['wyde-root'] == None:
        return False

    return True

def InitializeErrorList():
    if gold_globals.goldErrorsView == None:
        gold_globals.goldErrorsView = sublime.active_window().create_output_panel("golderrors")

def InitializeEnvironnement(path):
    # TODO : use env variables or project setting to initialize env. ?
    # TODO : Fix the path (\dll or \dll.debug)
    gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + sys._getframe().f_code.co_name)
    gold_globals.hWamAPI = ctypes.cdll.LoadLibrary("eWamAPI.dll")
    request = b"""
        {   
            "eWamRequest":
            {   
                "myId":0,
                "myPid":0,
                "myUser":"Developer",
                "myVersion":"00.00",
                "myRequest":"openEwamAdaptor",
                "myParams":""
            }
        }
    """
    # TODO: handle initialization error
    result = ctypes.c_char_p( gold_globals.hWamAPI.execEwamCmd(0, request) )

    InitializeErrorList()

    # TODO: if result OK : say ok, otherwise say error + message_error to inform user
    gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + sys._getframe().f_code.co_name)

def GetPath():
   projName = sublime.active_window().project_file_name()
   if projName == None:
      return None
   else:
      return sublime.active_window().project_data()['wyde-root']

def Parse(view):
   gold_helpers.LogAndStatusMessage("--> " + __name__ + ": " + sys._getframe().f_code.co_name)

   className = view.name().split('.')[0]
   source = view.substr(sublime.Region(0, view.size())).translate(str.maketrans( {'"': '\\\"' } ))
   request = b"""
   {
      "eWamRequest":
      {
         "myId":0,
         "myPid":0,
         "myUser":"Developer",
         "myVersion":"00.00",
         "myRequest":"parseSource",
         "myParams":
         {
            "classId":0,
            "classNsid":0,
            "classVersion":0,
            "className":\"""" + className.encode('ascii') + b"""\",
            "classSrc":\"""" + source.encode('ascii') + b"""\",
            "ancestor":"aApplicativeRoot"
         }
      }
   }
   """

   #print(request.decode('ascii'))
   result = ctypes.c_char_p( gold_globals.hWamAPI.execEwamCmd(0, request) )
   print(result.value.decode('ascii'))

   #jsonObj = json.loads(result.value.decode('ascii').replace('\r\n', '\n'))
   #jsonObj = sublime.decode_value(result.value.decode('ascii').replace('\r\n', '\\n'))
   jsonObj = sublime.decode_value(result.value.decode('ascii'))

   gold_helpers.LogAndStatusMessage("<-- " + __name__ + ": " + sys._getframe().f_code.co_name)

   #return jsonObj['eWamReply']['myResult'].replace('\r\n', '\\n')
   #print(jsonObj['eWamReply']['myResult'].replace('\r\n', '\\n'))
   #return jsonObj['eWamReply']['myResult']
   return jsonObj
