;aERS_Repository

class aERS_Repository (aWT_RestResource) 

uses aEntity, aERS_MMBrowserAPI

type tMMResponseWithState : record (tEntity)
   state : CString
endRecord
type tEntitiesWithState : sequence [UnBounded] of tMMResponseWithState


;@method POST
procedure Synchronize
   uses aInOutPresentor
   
   var thePresentor : aInOutPresentor
   
   new(thePresentor)
   thePresentor.DoSyncAll
   dispose(thePresentor)
endProc 

;@method POST
procedure Deliver
   uses aClassDef, aInDeliverPresentor, Motor
   
   var c : aClassDef
   var ThePresentor : aInDeliverPresentor
   
   c = MetaModelEntity(aInDeliverPresentor)
   while c.Descendants.count > 0
      c = c.Descendants[0]
   endWhile
   ;
   ThePresentor = Motor.NewInst(c.Id)
   ThePresentor.Display
   dispose(ThePresentor)
endProc 

;@method POST
procedure CheckinAll
   uses aClassDef, aInDeliverPresentor, Motor
   
   var c : aClassDef
   var ThePresentor : aInDeliverPresentor
   
   c = MetaModelEntity(aInDeliverPresentor)
   while c.Descendants.count > 0
      c = c.Descendants[0]
   endWhile
   ;
   ThePresentor = Motor.NewInst(c.Id)
   ThePresentor.RefreshCategories
   ThePresentor.checkInAll
   dispose(ThePresentor)
endProc 

;@method POST
procedure DeliverAll
   uses aClassDef, aInDeliverPresentor, Motor
   
   var c : aClassDef
   var ThePresentor : aInDeliverPresentor
   
   c = MetaModelEntity(aInDeliverPresentor)
   while c.Descendants.count > 0
      c = c.Descendants[0]
   endWhile
   ;
   ThePresentor = Motor.NewInst(c.Id)
   ThePresentor.RefreshCategories
   ThePresentor.DeliverAll
   dispose(ThePresentor)
endProc 

;@method POST
;@url */api/rest/Repository/status
function Status return tEntitiesWithState
   uses aClassDef, aInDeliverPresentor, Motor, aInDeliverCategory, lib, aWT_SequenceTypeExtension, 
      aSequenceType
   
   var c : aClassDef
   var ThePresentor : aInDeliverPresentor
   var cat : aInDeliverCategory
   var entity : aEntity
   var rep : tMMResponseWithState
   
   c = MetaModelEntity(aInDeliverPresentor)
   while c.Descendants.count > 0
      c = c.Descendants[0]
   endWhile
   ;
   ThePresentor = Motor.NewInst(c.Id)
   ThePresentor.RefreshCategories
   forEach cat in ThePresentor.categories
      forEach entity in cat.Entities
         rep.name = entity.Name
         rep.state = cat.ModificationState(entity)
         rep.theType = entity.ClassDef.Name
         lib.SequenceType.Append(rep, _Result, _Result.type)
      endFor
   endFor
   dispose(ThePresentor)
endFunc 

