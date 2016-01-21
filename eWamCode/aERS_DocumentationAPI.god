;aERS_DocumentationAPI

class aERS_DocumentationAPI (aWT_RestResource) 

uses aWT_UrlDecorationServerRouter, aWT_JsonCollection, aMethodDesc, aType, aEntity, 
   aMethodType, aWT_RestRequest, aWT_RestResponse, aParameterDesc, aListOfInstances, 
   aFullObject, aRecordDesc, aWT_JsonValue

const cWF_401_UserNotLogged = 'User not connected or session time out, please reauthenticate and resend a token'
const cWF_404_UserNotAuthorized = 'You are not authorized to process this action, please contact your administrator'
const cWF_400_BadRequestFillValidError = 'Fill valid error raised an error - see error details in the response headers'
const cWF_500_ObjectNotChanged = 'Object Not Changed'

type tErrorCode : record
   code : CString
   error : CString
endRecord


procedure GetSchema(inOut OutJsonValue : aWT_JsonCollection, paramater : aType)
   uses aClassDef, Motor, aWT_JsonSchemaSerializer
   
   var Serializer : aWT_JsonSchemaSerializer
   var instance : aFullObject
   var varAddress : Pointer
   
   ; if paramater = MetaModelEntity(tSLI_ClientSynthesisInfo)
   ;NDE: do nothing until PT-150 is delivered
   ; else
   new(Serializer)
   if member(paramater, aClassDef)
      instance = Motor.NewInstFromName(paramater.Name)
      varAddress = @instance
   else
      varAddress = GetMem(paramater.VarSize)
   endIf
   if Serializer.SerializeAsJsonValue(OutJsonValue, varAddress, paramater)
   endIf
   if member(paramater, aClassDef)
      dispose(instance)
   else
      FreeMem(varAddress, paramater.VarSize)
   endIf
   dispose(Serializer)
   ; endIf
endProc 

procedure AppendDefaultResponses(toMethod : aWT_JsonCollection, methodAsCstring : CString, 
   successParamType : aType, inOut definitions : aListOfInstances)
   var responses : aWT_JsonCollection
   var collection : aWT_JsonCollection
   var schema : aWT_JsonCollection
   
   new(responses)
   ;;Responses
   new(collection)
   collection.AppendCString('description', 'The request has succeeded')
   if successParamType <> Nil
      new(schema)
      schema.AppendCString('$ref', '#/definitions/' + successParamType.Name)
      definitions.AppendInexistingObject(successParamType)
      collection.AppendValue('schema', schema)
   endIf
   responses.AppendValue('200', collection)
   ;
   new(collection)
   collection.AppendCString('description', cWF_401_UserNotLogged)
   responses.AppendValue('401', collection)
   ;
   new(collection)
   collection.AppendCString('description', cWF_404_UserNotAuthorized)
   responses.AppendValue('404', collection)
   ;
   if methodAsCstring <> 'get'
      new(collection)
      collection.AppendCString('description', cWF_400_BadRequestFillValidError)
      new(schema)
      schema.AppendCString('$ref', '#/definitions/' + MetaModelEntity(tErrorCode).Name)
      definitions.AppendInexistingObject(MetaModelEntity(tErrorCode))
      collection.AppendValue('schema', schema)
      responses.AppendValue('400', collection)
      ;;
      new(collection)
      collection.AppendCString('description', cWF_500_ObjectNotChanged)
      responses.AppendValue('500', collection)
   endIf
   ;;
   toMethod.AppendValue('responses', responses)
endProc 

function MethodInfoAsSwaggerPath(MethodLaunchInfo : tWT_MethodLaunchCandidate, inOut definitions : aListOfInstances, 
   theRouter : aWT_UrlDecorationServerRouter) return aWT_JsonCollection protected
   uses aEnumType, aWT_JsonArray, aWT_JsonText, aMethodImplem, lib, aWT_CStringTypeExtension, 
      aTextType, aIntType, aWT_TextTypeExtension, aClassDef, aWT_JsonStatement, aBooleanType
   
   var method : aWT_JsonCollection
   var collection : aWT_JsonCollection
   var schema : aWT_JsonCollection
   var tags : aWT_JsonArray
   var jsonArray : aWT_JsonArray
   var defs : aWT_JsonStatement
   var value : aWT_JsonText
   var implem : aMethodImplem
   var successParam : aType
   var description : Text
   var comment : Text
   var methodAsCstring : CString
   var paramType : aType
   var bodyParam : Boolean
   var parameter : aParameterDesc
   var res : CString
   var className : CString
   
   ;var index : Int4
   ;var l : Int4
   ;var pSubVar : tpPointer
   ;var preprocessor : aMethodDesc
   methodAsCstring = lib.CStringType.LowerCase(MethodLaunchInfo.HttpMethod.type.AsCString(@MethodLaunchInfo.HttpMethod))
   new(method)
   new(tags)
   new(value)
   className = MethodLaunchInfo.MethodDesc.myOwner.Name
   res = lib.CStringType.SubCString('_', className)
   value.SetTextWithCString(className)
   tags.AppendValue(value)
   method.AppendArray('tags', tags)
   ;
   new(jsonArray)
   forEach parameter in MethodLaunchInfo.MethodDesc.myType.myParameters
      if parameter.Name <> 'self'
         if parameter.Name = '_Result'
            successParam = parameter.myType
         else
            new(collection)
            collection.AppendCString('name', parameter.Name)
            if lib.TextType.SearchCString(parameter.Name, MethodLaunchInfo.UrlPattern, 
               0) > 0
               collection.AppendCString('in', 'path')
               collection.AppendBoolean('required', True)
            elseif methodAsCstring = 'get'
               collection.AppendCString('in', 'query')
               collection.AppendBoolean('required', False)
            else
               collection.AppendCString('in', 'body')
               bodyParam = True
               collection.AppendBoolean('required', False)
            endIf
            paramType = parameter.myType
            if member(paramType, aIntType)
               collection.AppendCString('type', 'integer')
            elseif member(paramType, aBooleanType)
               collection.AppendCString('type', 'boolean')
            elseif (member(paramType, aClassDef) or member(paramType, aRecordDesc)) and 
               (lib.TextType.SearchCString(parameter.Name, MethodLaunchInfo.UrlPattern, 
               0) < 0) and (methodAsCstring <> 'get')
               new(schema)
               schema.AppendCString('$ref', '#/definitions/' + paramType.Name)
               definitions.AppendInexistingObject(paramType)
               collection.AppendValue('schema', schema)
            else
               collection.AppendCString('type', 'string')
            endIf
            if parameter.myText <> ''
               collection.AppendCString('description', parameter.myText)
            else
               collection.AppendText('description', parameter.Comment)
            endIf
            jsonArray.AppendValue(collection)
         endIf
      endIf
   endFor
   if (methodAsCstring <> 'get') and not bodyParam
      new(collection)
      collection.AppendCString('name', 'body')
      collection.AppendCString('in', 'body')
      collection.AppendBoolean('required', False)
      collection.AppendCString('type', 'string')
      jsonArray.AppendValue(collection)
   endIf
   method.AppendArray('parameters', jsonArray)
   ;;
   if successParam = Nil
      successParam = MethodLaunchInfo.MethodDesc.myType.ReturnType
   endIf
   self.AppendDefaultResponses(method, methodAsCstring, successParam, definitions)
   ;
   implem = MethodLaunchInfo.MethodDesc.myCurImplem
   ; implem.RegenerateTextFromIr
   method.AppendCString('summary', MethodLaunchInfo.UrlPattern.type.AsCString(@MethodLaunchInfo.UrlPattern))
   description := implem.Comment
   method.AppendText('description', description)
   ;  endIf
   ;
   _Result = method
   description := ''
   comment := ''
   ;
endFunc 

function GetAPIVersion return CString
   _Result = '0.0.1'
endFunc 

function getAPIInfo return aWT_JsonCollection
   var contact : aWT_JsonCollection
   
   new(_Result)
   _Result.AppendCString('description', 'This is is the rest API for eWam')
   _Result.AppendCString('version', self.GetAPIVersion)
   _Result.AppendCString('title', 'eWam Rest API')
   new(contact)
   contact.AppendCString('name', 'API Team')
   contact.AppendCString('url', 'http://www.wynsure.com')
   contact.AppendCString('email', 'support@wynsure.com')
   _Result.AppendValue('contact', contact)
endFunc 

;@method GET
;@url */api/rest/documentation
procedure GetSwaggerDocumentation
   uses aWT_JsonArray, aTextType, lib, aClassDef, aWT_CStringTypeExtension, aEnumType, 
      aWT_JsonStatement, aWT_TextTypeExtension
   
   var JsonCollection : aWT_JsonCollection
   var endPoint : aWT_JsonCollection
   var JsonResult : aWT_JsonCollection
   var paths : aWT_JsonCollection
   var tags : aWT_JsonArray
   var theRouter : aWT_UrlDecorationServerRouter
   var MethodLaunchInfo : tWT_MethodLaunchCandidate
   var tag : aWT_JsonCollection
   var RequestURL : Text
   var baseurl : Text
   var listOfTags : aListOfInstances
   var definitions : aListOfInstances
   var jsonDefinitions : aWT_JsonCollection
   var classdef : aClassDef
   var method : CString
   var res : CString
   var className : CString
   var definition : aType
   var defs : aWT_JsonStatement
   var defsValue : aWT_JsonValue
   var value : aWT_JsonStatement
   
   ;
   RequestURL := self.Request.Url
   lib.TextType.SubCString(baseurl, '/api/', RequestURL)
   lib.TextType.SubCString(RequestURL, 'http://', baseurl)
   theRouter = Pointer(self.Router)
   if member(theRouter, aWT_UrlDecorationServerRouter)
      new(JsonResult)
      new(listOfTags)
      new(definitions)
      JsonResult.AppendCString('swagger', '2.0')
      JsonResult.AppendCString('host', baseurl.type.AsCString(@baseurl))
      JsonResult.AppendCString('basePath', '/api')
      JsonResult.AppendValue('info', self.getAPIInfo)
      new(paths)
      ;
      forEach MethodLaunchInfo in theRouter.MethodLaunchInfoList
         ;theRouter.FillRequestInfo(Request)
         ;if member(theRouter, aSRF_UrlDecorationServerRouter)
         ;   aSRF_UrlDecorationServerRouter(theRouter).FillRequestInfoPublic(MethodLaunchInfo)
         ;endIf
         className = MethodLaunchInfo.MethodDesc.myOwner.Name
         RequestURL := MethodLaunchInfo.UrlPattern
         lib.TextType.SubCString(baseurl, '/api', RequestURL)
         if not RequestURL.type.IsBlank(@RequestURL)
            method = lib.CStringType.LowerCase(MethodLaunchInfo.HttpMethod.type.AsCString(@MethodLaunchInfo.HttpMethod))
            JsonCollection = self.MethodInfoAsSwaggerPath(MethodLaunchInfo, definitions, 
               theRouter)
            if paths.ExistName(RequestURL.type.AsCString(@RequestURL))
               endPoint = aWT_JsonCollection(paths.GetStatementByName(RequestURL.type.AsCString(@RequestURL)).GetValue)
               endPoint.AppendValue(method, JsonCollection)
            else
               new(endPoint)
               endPoint.AppendValue(method, JsonCollection)
               paths.AppendValue(RequestURL.type.AsCString(@RequestURL), endPoint)
            endIf
            listOfTags.AppendInexistingObject(MethodLaunchInfo.MethodDesc.myOwner)
         endIf
      endFor
      new(tags)
      forEach classdef in listOfTags
         new(tag)
         className = classdef.Name
         res = lib.CStringType.SubCString('_', className)
         tag.AppendCString('name', className)
         tag.AppendText('description', classdef.Comment)
         tags.AppendValue(tag)
      endFor
      JsonResult.AppendArray('tags', tags)
      JsonResult.AppendValue('paths', paths)
      new(jsonDefinitions)
      forEach definition in definitions
         new(JsonCollection)
         self.GetSchema(JsonCollection, definition)
         defs = JsonCollection.GetStatementByName('definitions')
         if defs = Nil
            jsonDefinitions.AppendValue(definition.Name, JsonCollection)
         else
            JsonCollection.RemoveStatementWithSameName(defs)
            ;value=defs.Geawt_sta
            jsonDefinitions.AppendValue(definition.Name, JsonCollection)
            defsValue = defs.GetValue
            if (defsValue <> Nil) and member(defsValue, aWT_JsonCollection)
               forEach value in aWT_JsonCollection(defsValue).Descendants
                  jsonDefinitions.AppendValue(value.GetNameAsCString, value.GetValue)
               endFor
            endIf
         endIf
      endFor
      ;
      JsonResult.AppendValue('definitions', jsonDefinitions)
      JsonResult.asJsonFragment(self.Response.Body)
      dispose(JsonResult)
      dispose(listOfTags)
      dispose(definitions)
   endIf
endProc 

