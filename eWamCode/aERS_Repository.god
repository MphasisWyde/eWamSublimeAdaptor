;aERS_Repository

class aERS_Repository (aWT_RestResource) 


procedure Deliver
   uses aWideIde, aUser, aClassDef, aInDeliverPresentor, Risky, aWideContext, Motor
   
   var theIde : aWideIde
   var theUser : aUser
   var c : aClassDef
   var IDE : aWideIde
   var ThePresentor : aInDeliverPresentor
   
   ;var IDEOption : aWxMultiUserOptions
   ; Overriding reason
   ; - instanciate any custo of aInDeliverPresentor
   theIde = Risky.GetIDE
   theUser = aWideContext(theIde.Context).theLoggedUser
   if (theUser.userGroup <> Guest) and (theUser.userGroup <> Admin)
      c = MetaModelEntity(aInDeliverPresentor)
      IDE = Risky.GetIDE
      ; IDEOption = aWxMultiUserOptions(IDE.GetOptionOf(MetaModelEntity(aWxMultiUserOptions).Id))
      ;self.ChangeInDeliverCategroryScen(IDEOption.UseBaseDeliverCheckInPresentor)
      ;if not IDEOption.UseBaseDeliverCheckInPresentor
      ;   while c.Descendants.count > 0
      ;      c = c.Descendants[0]
      ;   endWhile
      ;endIf
      ThePresentor = Motor.NewInst(c.Id)
      ThePresentor.Display
      dispose(ThePresentor)
   endIf
endProc 

