;aERS_ModuleDefAPI

class aERS_ModuleDefAPI (aWT_RestResource) 

uses aModuleDef, aWT_RestResponse, aWT_HttpRoot, aWT_RestRequest, aScenario, aCUImplem, 
   aRecordDesc, aEntity, aModuleImplem

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
type tImplem : record
   name : CString
   ancestor : CString
   content : Text
endRecord


procedure GetOutgoingURLMappingForScenario(object : aScenario, inOut name : CString, 
   inOut scenarioName : CString)
   scenarioName = object.Name
   name = object.myOwner.Name
endProc 

procedure GetOutgoingURLMappingForCUImplem(object : aModuleImplem, inOut name : CString)
   name = object.Name
endProc 

procedure GetOutgoingURLMapping(object : aModuleDef, inOut name : CString)
   name = object.Name
endProc 

function GetMyScenario(name : aModuleDef, scenarioName : IDEName) return aLightObject
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

procedure Deliver(name : aModuleDef)
   uses wWamIde
   
   if name = Nil
      self.Response.StatusCode = HTTP_STATUS_NOT_FOUND_404
   else
      wWamIde.Deliver(name)
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

procedure ManageReimplem(name : aModuleDef)
   uses wWamIde
   
   if name = Nil
      self.Response.StatusCode = HTTP_STATUS_NOT_FOUND_404
   else
      wWamIde.ManageReimplem(name, Modification)
   endIf
endProc 

function Get(name : aModuleDef) return tImplem
   if name = Nil
      self.Response.StatusCode = HTTP_STATUS_NOT_FOUND_404
   else
      name.myCurImplem.RegenerateTextFromIr
      _Result.content := name.myCurImplem.myTextFromMM
      _Result.name = name.Name
      _Result.ancestor = name.DerivesFrom.Name
   endIf
endFunc 

function _ModifyImplem(name : aModuleDef, parseOnly : Boolean, body : tImplem) return tImplem
   uses aClassPreparer, aBooleanType, lib, aWT_SequenceTypeExtension, aSequenceType, 
      JSON
   
   var myClassPreparer : aClassPreparer
   var myModule : aModuleDef
   var myError : tError
   var myErrors : tErrors
   var parseError : tpInternalParseError
   var myModuleImplem : aModuleImplem
   var _parseOnly : Boolean
   var _param : CString
   
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
      myClassPreparer.CodeText := body.content
      myClassPreparer.TestSyntax
      myModuleImplem = aModuleImplem(myModule.myCurImplem)
      if myClassPreparer.ParsingStatus = SyntaxOk
         _Result.content := myModuleImplem.myTextFromMM
         _Result.name = name.Name
         _Result.ancestor = name.DerivesFrom.Name
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

function Parse(name : aModuleDef, body : tImplem) return tImplem
   _Result = self._ModifyImplem(name, True, body)
endFunc 

function Modify(name : aModuleDef, body : tImplem) return tImplem
   _Result = self._ModifyImplem(name, False, body)
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

procedure Create(body : tImplem)
   uses aWT_JsonSerializer, aClassDef, Motor, xClassOrModuleMaker
   
   var myModule : aModuleDef
   var src : Text
   var myJsonSerializer : aWT_JsonSerializer
   var ancestor : aClassDef
   var newclass : aClassDef
   var name : CString
   
   ;
   src := body.content
   name = body.name
   ancestor = Motor.FindModuleOrClassFromName(body.ancestor)
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

