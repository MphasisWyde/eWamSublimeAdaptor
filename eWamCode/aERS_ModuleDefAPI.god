;aERS_ModuleDefAPI

class aERS_ModuleDefAPI (aWT_RestResource) 

uses aModuleDef, aWT_RestResponse, aWT_HttpRoot, aWT_RestRequest, aScenario, aCUImplem, 
   aRecordDesc, aEntity

type tIDEEntities : sequence [UnBounded] of IDEName
type tEntityStatus : record
   checkedOut : Boolean
endRecord
type tInternalParseError : record
   theVMT : Pointer
   Wording : String255
   LineNumber : Int4
   CharPos : Int4
   ErrorNum : Int4
endRecord
type tpInternalParseError : .tInternalParseError
type tError : record
   line : Int4
   offSet : Int2
   msg : CString
endRecord
type tErrors : sequence [UnBounded] of tError


procedure GetOutgoingURLMappingForScenario(object : aScenario, inOut name : CString, 
   inOut scenarioName : CString)
   scenarioName = object.Name
   name = object.myOwner.Name
endProc 

procedure GetOutgoingURLMappingForCUImplem(object : aCUImplem, inOut name : CString)
   name = object.Name
endProc 

procedure GetOutgoingURLMapping(object : aModuleDef, inOut name : CString)
   name = object.Name
endProc 

function GetMyScenario(name : aModuleDef, scenarioName : IDEName) return aScenario
   if name = Nil
      self.Response.StatusCode = HTTP_STATUS_NOT_FOUND_404
   else
      _Result = name.ScenarioFromName(scenarioName)
   endIf
endFunc 

function entityStatus(name : aModuleDef) return tEntityStatus
   uses aClassPreparer
   
   var myClassPreparer : aClassPreparer
   var response : Text
   
   if name = Nil
      self.Response.StatusCode = HTTP_STATUS_NOT_FOUND_404
   else
      new(myClassPreparer)
      myClassPreparer.Name = name.Name
      _Result.checkedOut = myClassPreparer.IsOwnedByLoggedUser
      dispose(myClassPreparer)
   endIf
endFunc 

function GetScenarios(name : aModuleDef) return tIDEEntities
   uses lib, aWT_SequenceTypeExtension, aSequenceType
   
   var theScenario : aScenario
   
   if name = Nil
      self.Response.StatusCode = HTTP_STATUS_NOT_FOUND_404
   else
      forEach theScenario in name.AvailableScenarios
         lib.SequenceType.Append(theScenario.Name, _Result, _Result.type)
      endFor
   endIf
endFunc 

function GetDescendants(name : aModuleDef) return tIDEEntities
   uses aClassDef, lib, aWT_SequenceTypeExtension, aSequenceType
   
   var descendant : aClassDef
   
   if name = Nil
      self.Response.StatusCode = HTTP_STATUS_NOT_FOUND_404
   else
      if member(name, aClassDef)
         forEach descendant in aClassDef(name).Descendants
            lib.SequenceType.Append(descendant.Name, _Result, _Result.type)
         endFor
      endIf
   endIf
endFunc 

procedure CheckOut(name : aModuleDef)
   uses wWamIde
   
   if name = Nil
      self.Response.StatusCode = HTTP_STATUS_NOT_FOUND_404
   else
      wWamIde.CheckOut(name)
   endIf
endProc 

procedure CheckIn(name : aModuleDef)
   uses wWamIde
   
   if name = Nil
      self.Response.StatusCode = HTTP_STATUS_NOT_FOUND_404
   else
      wWamIde.CheckIn(name)
   endIf
endProc 

procedure Get(name : aModuleDef)
   if name = Nil
      self.Response.StatusCode = HTTP_STATUS_NOT_FOUND_404
   else
      name.myCurImplem.RegenerateTextFromIr
      self.Response.Body := name.myCurImplem.myTextFromMM
      self.Response.AppendHttpHeader('Content-Type', 'Application/text')
   endIf
endProc 

function Post(name : aModuleDef) return Boolean
   uses aClassPreparer, aModuleImplem, lib, aWT_SequenceTypeExtension, aSequenceType, 
      JSON, aBooleanType
   
   var myClassPreparer : aClassPreparer
   var myModule : aModuleDef
   var myError : tError
   var myErrors : tErrors
   var parseError : tpInternalParseError
   var myModuleImplem : aModuleImplem
   var _parseOnly : Boolean
   var _param : CString
   var parseOnly : Boolean
   
   _param = self.Request.GetParameterAsCString('parseOnly')
   if _parseOnly.type.ConvertFromCString(_param, @_parseOnly)
   endIf
   myModule = name
   if myModule = Nil
      self.Response.StatusCode = HTTP_STATUS_NOT_FOUND_404
   else
      ;;;
      ;;
      new(myClassPreparer)
      myClassPreparer.Name = myModule.Name
      myClassPreparer.Ancestor = myModule.DerivesFrom.Name
      myClassPreparer.CodeText := self.Request.Body
      myClassPreparer.TestSyntax
      myModuleImplem = aModuleImplem(myModule.myCurImplem)
      if myClassPreparer.ParsingStatus = SyntaxOk
         self.Response.Body := myModuleImplem.myTextFromMM
         ;Save the class
         if not _parseOnly
            if myClassPreparer.IsOwnedByLoggedUser
               myClassPreparer.StoreClass
            else
               self.Response.StatusCode = HTTP_STATUS_BAD_REQUEST_400
               self.Response.StatusMessage = 'please check out the class. It parses but it cannot be saved'
            endIf
         endIf
      else
         forEach parseError in myModuleImplem.ParseErrors
            myError.line = parseError.LineNumber
            myError.offSet = parseError.CharPos
            myError.msg = parseError.Wording
            lib.SequenceType.Append(myError, myErrors, myErrors.type)
         endFor
         self.Response.StatusCode = HTTP_STATUS_BAD_REQUEST_400
         self.Response.Body := JSON.StringifyEx(@myErrors, myErrors.type)
      endIf
      dispose(myClassPreparer)
   endIf
endFunc 

function getClassNameFromSource(inOut src : Text) return CString
   uses lib, aWT_TextTypeExtension, aTextType
   
   var startingPos : Int4
   var endingPos : Int4
   var endingStr : CString
   var className : Text
   var classNameStr : CString
   
   startingPos = 2
   endingStr = ' '
   endingPos = lib.TextType.SearchCString(endingStr, src, startingPos)
   lib.TextType.SubStr(className, src, startingPos, endingPos - startingPos)
   classNameStr = className.type.AsCString(@className)
   className := ''
   return classNameStr
endFunc 

function getAncestorNameFromSource(inOut src : Text) return CString
   uses lib, aWT_TextTypeExtension, aTextType
   
   var startingPos : Int4
   var endingPos : Int4
   var endingStr : CString
   var className : Text
   var classNameStr : CString
   
   startingPos = lib.TextType.SearchCString('(', src, startingPos) + 1
   endingPos = lib.TextType.SearchCString(')', src, startingPos)
   lib.TextType.SubStr(className, src, startingPos, endingPos - startingPos)
   classNameStr = className.type.AsCString(@className)
   className := ''
   return classNameStr
endFunc 

procedure Put(body : Text)
   uses aWT_JsonSerializer, aClassDef, Motor, xClassOrModuleMaker
   
   var myModule : aModuleDef
   var src : Text
   var myJsonSerializer : aWT_JsonSerializer
   var ancestor : aClassDef
   var newclass : aClassDef
   var name : CString
   
   ;
   src := self.Request.Body
   name = self.getClassNameFromSource(src)
   ;Save the class
   ancestor = Motor.FindModuleOrClassFromName(self.getAncestorNameFromSource(src))
   if (ancestor <> Nil) and (name <> '')
      if xClassOrModuleMaker.CreateClassOrModuleWithText(ancestor, name, src, newclass, 
         False)
      else
         self.Response.StatusCode = HTTP_STATUS_BAD_REQUEST_400
      endIf
   else
      self.Response.StatusCode = HTTP_STATUS_BAD_REQUEST_400
      self.Response.StatusMessage = 'No valid ancestor or class name'
   endIf
   src := ''
endProc 

