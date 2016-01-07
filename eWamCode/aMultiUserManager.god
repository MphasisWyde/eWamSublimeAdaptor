; aMultiUserManager (aSystemService) (Def Version:3) (Implem Version:3)

class aMultiUserManager (aSystemService) 

uses aSystemHttpTransaction, aLightEvent, aSystemServiceManager

type tEvents : sequence [UnBounded] of aLightEvent


procedure GeteWamLogs(transaction : aSystemHttpTransaction)
   uses aWideContext, aWideIde, Risky, xTGVTricks, aUser, aInOutPresentor, aRefDevHistoryPresentor, 
      JSON, aSequenceType, __Reserved__100481360
   
   const mlFromRefConfig = 'FromRefConfig' multiLang
   
   var curEvent : aLightEvent
   var theRefConfig : aRefConfig
   var context : aWideContext
   var myInOut : aInOutPresentor
   var theLoggedUser : aUser
   var response : Text
   var events : tEvents
   
   context = aWideContext(aWideIde(Risky.GetIDE).Context)
   theLoggedUser = context.theLoggedUser
   if theLoggedUser <> Nil
      if context.OpenRefDevDB
         theRefConfig = context.GetRefConfig
         new(myInOut)
         myInOut.DBMgrForRefDev = xTGVTricks.DBMgrForTGV(4)
         ;
         myInOut.Name = mlFromRefConfig
         myInOut.historyCount = 20
         myInOut.theRefConfig = theRefConfig
         myInOut.theLoggedUser = theLoggedUser
         myInOut.InitHistory
         myInOut.RefreshHistory(True)
         forEach curEvent in myInOut.Historian.tmpList
            events[-1] = curEvent
         endFor
         response = JSON.StringifyEx(@events, events.type)
         transaction.SetResponseBodyText(response)
         context.CloseRefDevDB
         ; dispose(jsonArray)
         dispose(myInOut)
      endIf
   endIf
endProc 

function InitService(manager : aSystemServiceManager, something : CString) return Boolean
   uses aSystemServiceMethod, aMethodDesc
   
   var m : aSystemServiceMethod
   
   m = manager.InstallMethod('http', 'refbasehistory', self, MetaModelEntity(aMultiUserManager.GeteWamLogs))
endFunc 

