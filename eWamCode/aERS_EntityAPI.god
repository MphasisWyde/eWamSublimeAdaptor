;aERS_EntityAPI

class aERS_EntityAPI (aWT_RestResource) 

uses aEntity, aScenario


procedure GetOutgoingURLMapping(object : aEntity, inOut ownerName : CString, inOut name : CString)
   name = object.Name
   if object.myOwner <> Nil
      ownerName = object.myOwner.Name
   else
      ownerName = 'nil'
   endIf
endProc 

function FindEntity(ownerName : CString, name : CString) return aEntity
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

function UIInteractEntity(ownerName : CString, name : CString) return aEntity
   _Result = self.FindEntity(ownerName, name)
   if _Result <> Nil
      if _Result.Interact(Nil, Consultation, True) = rValid
      endIf
   endIf
endFunc 

function GetEntity(ownerName : CString, name : CString) return aEntity
   ;
   _Result = self.FindEntity(ownerName, name)
endFunc 

