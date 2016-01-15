;aERS_MMBrowserAPI

class aERS_MMBrowserAPI (aWT_RestResource) 

uses aEntity, aWT_RestRequest, aWT_UrlDecorationServerRouter, aWT_MMNode

type tMMResponse : record
   name : IDEName
   theType : IDEName
   location : Text
endRecord
type tEntities : sequence [UnBounded] of tMMResponse


function GetBooleanParamValue(param : CString) return Boolean
   uses aBooleanType
   
   var value : CString
   
   value = self.Request.GetParameterAsCString(param)
   if not _Result.type.ConvertFromCString(value, @_Result)
      _Result = True
   endIf
endFunc 

;@url */api/rest/searchEntities
function searchEntities(q : CString, m : Int4, _class : Boolean, _module : Boolean, 
   _method : Boolean, _overrideMethod : Boolean, _variable : Boolean, _constant : Boolean, 
   _scenario : Boolean, _parameter : Boolean, _other : Boolean) return tEntities
   uses Motor, aClassDef, aMMBrowser, lib, aWT_SequenceTypeExtension, aSequenceType, 
      aIntType, aWT_UrlDecorationSettings
   
   var myMMBrowser : aMMBrowser
   var result : aEntity
   var response : Text
   var MMResponse : tMMResponse
   var _q : CString
   var _param : CString
   var _m : Int4
   var node : aWT_MMNode
   
   _q = self.Request.GetParameterAsCString('q')
   _param = self.Request.GetParameterAsCString('m')
   if (_param = '') or not m.type.ConvertFromCString(_param, @_m)
      _m = 100
   endIf
   ;
   new(myMMBrowser)
   myMMBrowser.CleanUpFoundEntities
   Motor.SetCurrentNsIdContext(13) ;cDevNSIdContext
   ;
   myMMBrowser.Criterium = _q + '*'
   ;
   if self.GetBooleanParamValue('_class')
      myMMBrowser.BrowseAbleEntitys += [mClass]
   endIf
   if self.GetBooleanParamValue('_module')
      myMMBrowser.BrowseAbleEntitys += [mModule]
   endIf
   if self.GetBooleanParamValue('_method')
      myMMBrowser.BrowseAbleEntitys += [mMethod]
   endIf
   if self.GetBooleanParamValue('_overrideMethod')
      myMMBrowser.BrowseAbleEntitys += [mOverrideMethod]
   endIf
   if self.GetBooleanParamValue('_variable')
      myMMBrowser.BrowseAbleEntitys += [mVariable]
   endIf
   if self.GetBooleanParamValue('_constant')
      myMMBrowser.BrowseAbleEntitys += [mConstant]
   endIf
   if self.GetBooleanParamValue('_scenario')
      myMMBrowser.BrowseAbleEntitys += [mScenario]
   endIf
   if self.GetBooleanParamValue('_parameter')
      myMMBrowser.BrowseAbleEntitys += [mParameter]
   endIf
   if self.GetBooleanParamValue('_other')
      myMMBrowser.BrowseAbleEntitys += [mOtherSharableObjects]
   endIf
   ;
   myMMBrowser.ExecutingSelection = True
   myMMBrowser.BrowseAbleEntitys += [mType, mConstant]
   myMMBrowser.MaxCountInFoundEntities = _m
   myMMBrowser.Select
   forEach result in myMMBrowser.FoundEntities
      MMResponse.name = result.Name
      MMResponse.theType = result.ClassDef.Name
      new(node)
      node.VarAddress = @result
      node.VarType = result.type
      self.Router.Settings.GetNodeURL(MMResponse.location, node)
      dispose(node)
      ;GetInstanceURL(MMResponse.location, result)
      lib.SequenceType.Append(MMResponse, _Result, _Result.type)
   endFor
endFunc 

