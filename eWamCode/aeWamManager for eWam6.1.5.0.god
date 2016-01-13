; aeWamManager (aSystemService) (Def Version:3) (Implem Version:5)

class aeWamManager (aSystemService) 

uses aSystemHttpTransaction, aSystemServiceManager, aModuleDef, aEntity, aWideContext, 
   aRecordDesc, aWT_TypeExtension, aScenario

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
type tEntityStatus : record
   checkedOut : Boolean
endRecord
type tRec : record
   x : Int4
   y : CString
endRecord
type tNamedEntities : sequence [UnBounded] of Text
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
      bundles[-1] := bundle.Name
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
   uses aMMBrowser, Motor, aTextType, JSON, aSequenceType
   
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
   myMMBrowser.BrowseAbleEntitys = [mClass, mModule, mMethod, mOverrideMethod, mVariable, 
      mType, mConstant]
   myMMBrowser.Select
   ;myMMBrowser.SelectFromClassId(MetaModelEntity(aClassDef).Id, MetaModelEntity(aClassDef).Id, 
   ;   False, mClass)
   forEach result in myMMBrowser.FoundEntities
      if result.myOwner <> Nil
         entities[-1] := result.myOwner.Name + '/' + result.Name
      else
         entities[-1] := result.Name
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

procedure OpenEntity(transaction : aSystemHttpTransaction)
   uses aTextType, Motor, aWT_SequenceTypeExtension, lib, aWT_TextTypeExtension, 
      aMMBrowser
   
   var name : CString
   var input : Text
   var output : tWT_TextSequence
   var Seq : tWT_TextSequence
   var criteria : CString
   var myMMBrowser : aMMBrowser
   var result : aEntity
   var response : Text
   var src : Text
   var entities : tNamedEntities
   var ownerName : IDEName
   var tmpName : IDEName
   var l : Int4
   
   input := transaction.HttpIdentifier
   Seq = lib.TextType.Explode(input, '/', c_unlimited)
   l = lib.SequenceType.Len(Seq)
   if l > 0
      src = Seq[l - 1]
      name = src.type.AsCString(@src)
   endIf
   if l > 1
      src = Seq[l - 2]
      ownerName = src.type.AsCString(@src)
   endIf
   ;
   new(myMMBrowser)
   transaction.HttpStatusCode = 200
   myMMBrowser.CleanUpFoundEntities
   Motor.SetCurrentNsIdContext(13) ;cDevNSIdContext
   ;
   myMMBrowser.Criterium = name
   myMMBrowser.ExecutingSelection = True
   myMMBrowser.BrowseAbleEntitys = [mClass, mModule, mMethod, mOverrideMethod, mVariable, 
      mType, mConstant]
   myMMBrowser.Select
   forEach result in myMMBrowser.FoundEntities
      if Upcase(ownerName) <> ''
         if result.myOwner <> Nil
            tmpName = result.myOwner.Name
            if Upcase(ownerName) = Upcase(tmpName)
               ; it is a redirect to eWam
               transaction.HttpStatusCode = 301
               if result.Interact(Nil, Consultation, True) = rValid
               endIf
               break
            endIf
         endIf
      else
         if member(result, aModuleDef) and (aModuleDef(result).myCurImplem <> Nil)
            self.Get(aModuleDef(result), transaction)
         else
            ; it is a redirect to eWam
            transaction.HttpStatusCode = 301
            if result.Interact(Nil, Consultation, True) = rValid
            endIf
         endIf
      endIf
   endFor
   ; response := ''
   dispose(myMMBrowser)
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

procedure DisplayIDEInfoViewer
   uses aWideIde, Risky
   
   var theIDE : aWideIde
   
   theIDE = Risky.GetIDE
   theIDE.DisplayWideComment
endProc 

procedure CloseIDEInfoViewer
   uses aWideIde, aUIAgent, Risky
   
   var theIDE : aWideIde
   var Agent : aUIAgent
   
   theIDE = Risky.GetIDE
   Agent = theIDE.GetUIAgentFromName('WideComment')
   Agent.Close(False)
endProc 

procedure EditScenario(thescenario : aScenario)
   uses wClassOrModuleMaker, aListofReftosType, xGraphMMModif
   
   var owner : aModuleDef
   var ownerProject : aModuleDef
   
   owner = aModuleDef(thescenario.myOwner)
   ownerProject = wClassOrModuleMaker.ProjectOfClassOrModule(owner)
   if ownerProject <> Nil
      xGraphMMModif.SetScenarioMakerModal(True)
      self.DisplayIDEInfoViewer ; temporary : need to have the IDE displayed
      if ownerProject.AvailableScenarios.type.ModifyAt(Nil, ownerProject, ownerProject.AvailableScenarios.RankOfOneVersionOfThisObject(thescenario), 
         @ownerProject.AvailableScenarios) <> Nil
      endIf
      self.CloseIDEInfoViewer ; temporary : need to have the IDE displayed
      xGraphMMModif.SetScenarioMakerModal(False)
      wClassOrModuleMaker.AcceptAndRegisterClassOrModule(ownerProject)
   else
      if thescenario.Interact(Nil, Consultation, True) = rValid
      endIf
   endIf
endProc 

procedure OpenScenario(transaction : aSystemHttpTransaction)
   uses aTextType, Motor, aWT_SequenceTypeExtension, lib, aWT_TextTypeExtension
   
   var name : CString
   var input : Text
   var output : tWT_TextSequence
   var Seq : tWT_TextSequence
   var result : aEntity
   var response : Text
   var src : Text
   var entities : tNamedEntities
   var ownerName : IDEName
   var tmpName : IDEName
   var l : Int4
   var moduledef : aModuleDef
   var thescenario : aScenario
   
   input := transaction.HttpIdentifier
   Seq = lib.TextType.Explode(input, '/', c_unlimited)
   l = lib.SequenceType.Len(Seq)
   if l > 0
      src = Seq[l - 1]
      name = src.type.AsCString(@src)
   endIf
   if l > 1
      src = Seq[l - 2]
      ownerName = src.type.AsCString(@src)
   endIf
   moduledef = Motor.FindModuleOrClassFromName(ownerName)
   if moduledef <> Nil
      thescenario = moduledef.GetScenarioFromName(name)
      if thescenario <> Nil
         ; 
         self.EditScenario(thescenario)
         transaction.HttpStatusCode = 200
      endIf
   endIf
endProc 

procedure Scenarios(transaction : aSystemHttpTransaction)
   uses JSON, aSequenceType
   
   var result : aScenario
   var response : Text
   var entities : tNamedEntities
   var myModule : aModuleDef
   
   myModule = self.GetModuleDef(transaction)
   if myModule <> Nil
      forEach result in myModule.AvailableScenarios
         entities[-1] := myModule.Name + '/' + result.Name
      endFor
      response = JSON.StringifyEx(@entities, entities.type)
      transaction.SetResponseBodyText(response)
      transaction.HttpStatusCode = 200
   endIf
endProc 

procedure Descendants(transaction : aSystemHttpTransaction)
   uses JSON, aClassDef, aSequenceType
   
   var result : aClassDef
   var response : Text
   var entities : tNamedEntities
   var myModule : aClassDef
   
   myModule = aClassDef(self.GetModuleDef(transaction))
   if (myModule <> Nil) and member(myModule, aClassDef)
      forEach result in myModule.Descendants
         entities[-1] := myModule.Name + '/' + result.Name
      endFor
      response = JSON.StringifyEx(@entities, entities.type)
      transaction.SetResponseBodyText(response)
      transaction.HttpStatusCode = 200
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

procedure GetOrModifyClassDef(transaction : aSystemHttpTransaction)
   uses aClassPreparer, Motor, aTextType, aModuleImplem, lib, aWT_SequenceTypeExtension, 
      aSequenceType, JSON
   
   var myClassPreparer : aClassPreparer
   var myModule : aModuleDef
   var src : Text
   var ancestor : CString
   var name : CString
   var theText : Text
   var Response : Text
   var myModuleImplem : aModuleImplem
   var myError : tError
   var myErrors : tErrors
   var parseError : tpInternalParseError
   
   ;
   name = transaction.HttpIdentifier.type.AsCString(@transaction.HttpIdentifier)
   myModule = Motor.FindModuleOrClassFromName(name)
   if myModule = Nil
      ; 
   else
      if transaction.HttpVerb = 'GET'
         self.Get(myModule, transaction)
      else
         new(myClassPreparer)
         myClassPreparer.Name = myModule.Name
         myClassPreparer.Ancestor = ancestor
         theText = transaction.GetRequestBodyText
         myClassPreparer.CodeText := theText
         myClassPreparer.TestSyntax
         myModuleImplem = aModuleImplem(myModule.myCurImplem)
         if myClassPreparer.ParsingStatus = SyntaxOk
            Response := myModuleImplem.myTextFromMM
            ;Save the class
            if myClassPreparer.IsOwnedByLoggedUser
               myClassPreparer.StoreClass
               transaction.HttpStatusCode = 200
            else
               transaction.HttpStatusCode = 403
            endIf
         else
            forEach parseError in myModuleImplem.ParseErrors
               myError.line = parseError.LineNumber
               myError.offSet = parseError.CharPos
               myError.msg = parseError.Wording
               lib.SequenceType.Append(myError, myErrors, myErrors.type)
            endFor
            transaction.HttpStatusCode = 403
            Response = JSON.StringifyEx(@myErrors, myErrors.type)
         endIf
         dispose(myClassPreparer)
         transaction.SetResponseBodyText(Response)
      endIf
   endIf
endProc 

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
   m = manager.InstallMethod('http', 'openEntity', self, MetaModelEntity(aeWamManager.OpenEntity))
   m = manager.InstallMethod('http', 'bundles', self, MetaModelEntity(aeWamManager.GetBundles))
   m = manager.InstallMethod('http', 'config', self, MetaModelEntity(aeWamManager.ManageConfig))
   m = manager.InstallMethod('http', 'entityStatus', self, MetaModelEntity(aeWamManager.entityStatus))
   m = manager.InstallMethod('http', 'scenarios', self, MetaModelEntity(aeWamManager.Scenarios))
   m = manager.InstallMethod('http', 'scenario', self, MetaModelEntity(aeWamManager.OpenScenario))
   m = manager.InstallMethod('http', 'descendants', self, MetaModelEntity(aeWamManager.Descendants))
   ;
   m = manager.InstallMethod('http', 'doHttp', self, MetaModelEntity(aeWamManager.HttpMethod))
   m = manager.InstallMethod('raw', 'doRaw', self, MetaModelEntity(aeWamManager.RawMethod))
   m = manager.InstallMethod('normal', 'method1', self, MetaModelEntity(aeWamManager.Method1))
   m = manager.InstallMethod('normal', 'method2', self, MetaModelEntity(aeWamManager.Method2))
endFunc 

