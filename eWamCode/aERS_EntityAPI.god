;aERS_EntityAPI

class aERS_EntityAPI (aWT_RestResource) 

uses aEntity, aScenario, aWT_RestResponse, aWT_HttpRoot, aERS_MMBrowserAPI, aWT_MMNode

type tDelivery : record
   bundle : CString
   delivery : CString
endRecord
type tDeliveries : sequence [UnBounded] of tDelivery


procedure GetOutgoingURLMapping(object : aEntity, inOut ownerName : CString, inOut name : CString)
   name = object.Name
   if object.myOwner <> Nil
      ownerName = object.myOwner.Name
   else
      ownerName = 'nil'
   endIf
endProc 

function _FindEntity(ownerName : CString, name : CString) return aEntity
   uses Motor, aWT_SequenceTypeExtension, aMMBrowser
   
   var input : Text
   var output : tWT_TextSequence
   var Seq : tWT_TextSequence
   var criteria : CString
   var myMMBrowser : aMMBrowser
   var result : aEntity
   var l : Int4
   
   ;
   new(myMMBrowser)
   myMMBrowser.CleanUpFoundEntities
   Motor.SetCurrentNsIdContext(13) ;cDevNSIdContext
   ;
   myMMBrowser.Criterium = name
   myMMBrowser.ExecutingSelection = True
   myMMBrowser.BrowseAbleEntitys = [mClass, mModule, mMethod, mOverrideMethod, mVariable, 
      mType, mConstant, mOtherSharableObjects]
   myMMBrowser.Select
   forEach result in myMMBrowser.FoundEntities
      if (Upcase(ownerName) <> 'NIL') and (ownerName <> '')
         if result.myOwner <> Nil
            if Upcase(ownerName) = Upcase(result.myOwner.Name)
               _Result = result
               break
            endIf
         endIf
      else
         _Result = result
      endIf
   endFor
   dispose(myMMBrowser)
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
   uses wClassOrModuleMaker, aListofReftosType, xGraphMMModif, aModuleDef
   
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

function UIInteractEntity([model(Text:'Name of the parent entity. Use ''Nil'' for a non owned entity.')] ownerName : CString, 
   [model(Text:'Exact Name of the entity to search')] name : CString) return aLightObject
   _Result = self._FindEntity(ownerName, name)
   if _Result <> Nil
      if _Result.Interact(Nil, Consultation, True) = rValid
      endIf
   endIf
endFunc 

;@method GET
;@URL */api/rest/entity/{ownerName}/{name}
function GetEntity([model(Text:'Name of the parent entity. Use ''Nil'' for a non owned entity.')] ownerName : CString, 
   [model(Text:'Exact Name of the entity to search')] name : CString) return aLightObject
   ;
   _Result = self._FindEntity(ownerName, name)
endFunc 

;@method GET
;@URL */api/rest/entity/{ownerName}/{name}/deliveries
function GetDeliveries([model(Text:'Name of the parent entity. Use ''Nil'' for a non owned entity.')] ownerName : CString, 
   [model(Text:'Exact Name of the entity to search')] name : CString) return tDeliveries
   uses ERS_IDEAPI
   
   var entity : aEntity
   
   entity = self._FindEntity(ownerName, name)
   if entity <> Nil
      _Result = ERS_IDEAPI._SearchInBundles(entity)
   endIf
endFunc 

;@method GET
;@URL */api/rest/entity/{ownerName}/{name}/WhereUsed
function WhereUsed([model(Text:'Name of the parent entity. Use ''Nil'' for a non owned entity.')] ownerName : CString, 
   [model(Text:'Exact Name of the entity to search')] name : CString) return tEntities
   uses aEntityMMViewer, ERS_IDEAPI
   
   var entity : aEntity
   var myMMViewer : aEntityMMViewer
   var MMResponse : tEntity
   var node : aWT_MMNode
   var result : aEntity
   
   entity = self._FindEntity(ownerName, name)
   _Result = ERS_IDEAPI.WhereUsed(entity)
endFunc 

;@method POST
;@URL */api/rest/entity/{ownerName}/{name}/CheckOut
procedure CheckOut([model(Text:'Name of the parent entity. Use ''Nil'' for a non owned entity.')] ownerName : CString, 
   [model(Text:'Exact Name of the entity to search')] name : CString)
   uses wWamIde, ERS_IDEAPI
   
   var entity : aEntity
   
   entity = self._FindEntity(ownerName, name)
   if entity = Nil
      self.Response.StatusCode = HTTP_STATUS_NOT_FOUND_404
   else
      wWamIde.CheckOut(entity)
      ERS_IDEAPI.SaveToFile(entity)
   endIf
endProc 

;@method POST
;@URL */api/rest/entity/{ownerName}/{name}/Deliver
procedure Deliver([model(Text:'Name of the parent entity. Use ''Nil'' for a non owned entity.')] ownerName : CString, 
   [model(Text:'Exact Name of the entity to search')] name : CString)
   uses wWamIde, ERS_IDEAPI
   
   var entity : aEntity
   
   entity = self._FindEntity(ownerName, name)
   if entity = Nil
      self.Response.StatusCode = HTTP_STATUS_NOT_FOUND_404
   else
      wWamIde.Deliver(entity)
      ERS_IDEAPI.SaveToFile(entity)
   endIf
endProc 

;@method POST
;@URL */api/rest/entity/{ownerName}/{name}/CheckIn
procedure CheckIn([model(Text:'Name of the parent entity. Use ''Nil'' for a non owned entity.')] ownerName : CString, 
   [model(Text:'Exact Name of the entity to search')] name : CString)
   uses wWamIde, ERS_IDEAPI
   
   var entity : aEntity
   
   entity = self._FindEntity(ownerName, name)
   if entity = Nil
      self.Response.StatusCode = HTTP_STATUS_NOT_FOUND_404
   else
      wWamIde.CheckIn(entity)
      ERS_IDEAPI.SaveToFile(entity)
   endIf
endProc 

