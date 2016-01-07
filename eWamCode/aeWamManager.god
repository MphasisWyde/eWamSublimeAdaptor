; aeWamManager (aSystemService) (Def Version:18) (Implem Version:32)

class aeWamManager (aSystemService) 

uses aSystemHttpTransaction, aSystemServiceManager, aModuleDef, aEntity, aWideContext, 
   aRecordDesc

type tEntityStatus : record
   checkedOut : Boolean
endRecord
type tRec : record
   x : Int4
   y : CString
endRecord
type tNamedEntities : sequence [UnBounded] of IDEName
type tEntities : sequence [UnBounded] of tRec

something : CString


procedure ManageConfig(transaction : aSystemHttpTransaction)
   uses aWideIde, Risky, aOption, JSON, aTextType
   
   var context : aWideContext
   var response : Text
   var option : aOption
   var isFirst : Boolean
   var name : CString
   
   isFirst = True
   context = aWideContext(aWideIde(Risky.GetIDE).Context)
   name = transaction.HttpIdentifier.type.AsCString(@transaction.HttpIdentifier)
   if name = ''
      response = JSON.Stringify(context)
   else
      forEach option in context.WydeOptions
         if Upcase(option.Name) = Upcase(name)
            response = JSON.Stringify(option)
         endIf
      endFor
   endIf
   ;
   transaction.SetResponseBodyText(response)
endProc 

procedure GetBundles(transaction : aSystemHttpTransaction)
   uses aPreparedDeliveriesBundleList, aDeliveriesBundlePreparer, xBundle, JSON, 
      aSequenceType
   
   var bundleList : aPreparedDeliveriesBundleList
   var bundle : aDeliveriesBundlePreparer
   var response : Text
   var isFirst : Boolean
   var bundles : tNamedEntities
   
   bundleList = xBundle.GetPreparedbundleCatalog
   forEach bundle in bundleList.DelBPreparers
      bundles[-1] = bundle.Name
   endFor
   response = JSON.StringifyEx(@bundles, bundles.type)
   transaction.SetResponseBodyText(response)
   ; response := ''
endProc 

procedure GetNameSuggestor(transaction : aSystemHttpTransaction)
   ; body
   ; position: line, column
endProc 

procedure SearchEntities(transaction : aSystemHttpTransaction)
   uses aMMBrowser, Motor, aClassDef, aTextType, JSON, aSequenceType
   
   var myMMBrowser : aMMBrowser
   var result : aEntity
   var name : CString
   var response : Text
   var entities : tNamedEntities
   
   new(myMMBrowser)
   transaction.HttpStatusCode = 200
   myMMBrowser.CleanUpFoundEntities
   Motor.SetCurrentNsIdContext(13) ;cDevNSIdContext
   name = transaction.HttpIdentifier.type.AsCString(@transaction.HttpIdentifier)
   ;
   myMMBrowser.Criterium = name + '*'
   ;
   myMMBrowser.ExecutingSelection = True
   myMMBrowser.SelectFromClassId(MetaModelEntity(aClassDef).Id, MetaModelEntity(aClassDef).Id, 
      False, mClass)
   forEach result in myMMBrowser.FoundEntities
      if member(result, aModuleDef)
         entities[-1] = result.Name
      else
         entities[-1] = result.Name
      endIf
   endFor
   response = JSON.StringifyEx(@entities, entities.type)
   transaction.SetResponseBodyText(response)
   ; response := ''
   dispose(myMMBrowser)
endProc 

procedure Get(name : aModuleDef, transaction : aSystemHttpTransaction)
   uses aCUImplem
   
   var src : Text
   
   if name = Nil
      ;self.Response.StatusCode = HTTP_STATUS_NOT_FOUND_404
   else
      if name.myCurImplem <> Nil
         name.myCurImplem.RegenerateTextFromIr
         src := name.myCurImplem.myTextFromMM
         transaction.SetResponseBodyText(src)
         transaction.HttpStatusCode = 200
         ; self.Response.Body := name.myCurImplem.myTextFromMM
         ; self.Response.AppendHttpHeader('Content-Type', 'Application/text')
      endIf
   endIf
endProc 

function GetModuleDef(transaction : aSystemHttpTransaction) return aModuleDef
   uses aTextType, Motor
   
   var name : CString
   
   name = transaction.HttpIdentifier.type.AsCString(@transaction.HttpIdentifier)
   _Result = Motor.FindModuleOrClassFromName(name)
   if _Result = Nil
      transaction.HttpStatusCode = 404
   endIf
endFunc 

procedure Scenarios(transaction : aSystemHttpTransaction)
   uses JSON, aSequenceType, aScenario
   
   var result : aScenario
   var response : Text
   var entities : tNamedEntities
   var myModule : aModuleDef
   
   myModule = self.GetModuleDef(transaction)
   if myModule <> Nil
      forEach result in myModule.AvailableScenarios
         if member(result, aModuleDef)
            entities[-1] = result.Name
         else
            entities[-1] = result.Name
         endIf
      endFor
      response = JSON.StringifyEx(@entities, entities.type)
      transaction.SetResponseBodyText(response)
   endIf
endProc 

procedure CheckIn(transaction : aSystemHttpTransaction)
   uses wWamIde
   
   var myModule : aModuleDef
   
   myModule = self.GetModuleDef(transaction)
   if myModule <> Nil
      wWamIde.CheckIn(myModule)
      transaction.HttpStatusCode = 200
   endIf
endProc 

procedure CheckOut(transaction : aSystemHttpTransaction)
   uses wWamIde
   
   var myModule : aModuleDef
   
   myModule = self.GetModuleDef(transaction)
   if myModule <> Nil
      wWamIde.CheckOut(myModule)
      transaction.HttpStatusCode = 200
   endIf
endProc 

function GetOrModifyClassDef(transaction : aSystemHttpTransaction) return Boolean
   uses aClassPreparer, Motor, aTextType
   
   var myClassPreparer : aClassPreparer
   var myModule : aModuleDef
   var src : Text
   var ancestor : CString
   var name : CString
   var theText : Text
   
   ;name : CString, body : Text
   ;hello
   ;var myJsonSerializer : aWT_JsonSerializer
   name = transaction.HttpIdentifier.type.AsCString(@transaction.HttpIdentifier)
   myModule = Motor.FindModuleOrClassFromName(name)
   if myModule = Nil
      _Result = False
      ; self.Response.StatusCode = HTTP_STATUS_NOT_FOUND_404
   else
      if transaction.HttpVerb = 'GET'
         self.Get(myModule, transaction)
      else
         new(myClassPreparer)
         myClassPreparer.Name = myModule.Name
         myClassPreparer.Ancestor = ancestor
         theText = transaction.GetRequestBodyText
         myClassPreparer.CodeText := theText
         ;Save the class
         if myClassPreparer.IsOwnedByLoggedUser
            myClassPreparer.StoreClass
            _Result = True
            transaction.HttpStatusCode = 200
         else
            _Result = False
         endIf
         dispose(myClassPreparer)
      endIf
   endIf
endFunc 

procedure HttpMethod(transaction : aSystemHttpTransaction)
   var response : Text
   var name : Text
   var value : Text
   var i : Int4
   
   WriteLn(response, transaction.HttpUrl)
   for i = 0 to transaction.GetRequestHeadersCount - 1
      if transaction.GetRequestHeader(i, name, value)
         Write(response, name, ' : ', value)
      endIf
   endFor
   WriteLn(response, transaction.GetRequestBodyText)
   transaction.SetResponseBodyText(response)
   transaction.HttpStatusCode = 200
endProc 

function RawMethod(identifier : Text, content : Text, inOut response : Text) return Int2
   Write(response, identifier, ' : ', content)
   return 0
endFunc 

function Method1(a : CString, b : Int4) return CString
   return self.something + a
endFunc 

function Method2(a : tRec) return tRec
   return a
endFunc 

procedure entityStatus(transaction : aSystemHttpTransaction)
   uses aClassPreparer, JSON
   
   var myModule : aModuleDef
   var myClassPreparer : aClassPreparer
   var status : tEntityStatus
   var response : Text
   
   myModule = self.GetModuleDef(transaction)
   if myModule <> Nil
      new(myClassPreparer)
      myClassPreparer.Name = myModule.Name
      status.checkedOut = myClassPreparer.IsOwnedByLoggedUser
      dispose(myClassPreparer)
      response = JSON.StringifyEx(@status, status.type)
      transaction.SetResponseBodyText(response)
   endIf
endProc 

function InitService(manager : aSystemServiceManager, something : CString) return Boolean
   uses aSystemServiceMethod, aMethodDesc
   
   var m : aSystemServiceMethod
   
   self.something = something
   m = manager.InstallMethod('http', 'aModuleDef', self, MetaModelEntity(aeWamManager.GetOrModifyClassDef))
   m = manager.InstallMethod('http', 'checkIn', self, MetaModelEntity(aeWamManager.CheckIn))
   m = manager.InstallMethod('http', 'checkOut', self, MetaModelEntity(aeWamManager.CheckOut))
   m = manager.InstallMethod('http', 'searchEntities', self, MetaModelEntity(aeWamManager.SearchEntities))
   m = manager.InstallMethod('http', 'bundles', self, MetaModelEntity(aeWamManager.GetBundles))
   m = manager.InstallMethod('http', 'config', self, MetaModelEntity(aeWamManager.ManageConfig))
   m = manager.InstallMethod('http', 'entityStatus', self, MetaModelEntity(aeWamManager.entityStatus))
   m = manager.InstallMethod('http', 'scenarios', self, MetaModelEntity(aeWamManager.Scenarios))
   ;
   m = manager.InstallMethod('http', 'doHttp', self, MetaModelEntity(aeWamManager.HttpMethod))
   m = manager.InstallMethod('raw', 'doRaw', self, MetaModelEntity(aeWamManager.RawMethod))
   m = manager.InstallMethod('normal', 'method1', self, MetaModelEntity(aeWamManager.Method1))
   m = manager.InstallMethod('normal', 'method2', self, MetaModelEntity(aeWamManager.Method2))
endFunc 

