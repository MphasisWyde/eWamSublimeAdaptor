;ERS_IDEAPI

module ERS_IDEAPI

uses aEntityMMViewer, aUIAgent, aEntity, aERS_MMBrowserAPI, aERS_EntityAPI, aDeliveriesBundle, 
   aWexConfigurationsToolsExtension


function FindEntityInDeliveriesBundle(thisDelBundle : aDeliveriesBundle, Entity : aEntity, 
   inOut CandidateRank : Int4) return Int4
   uses aDelivery
   
   var Delivery : aDelivery
   
   forEach Delivery in thisDelBundle.OwnedDeliveries using _Result
      CandidateRank = Delivery.Catalog.RankOfOneVersionOfThisObject(Entity)
      if CandidateRank >= 0
         exit
      endIf
   endFor
   return -1
endFunc 

function _SearchInBundles(entity : aEntity) return tDeliveries
   uses aPreparedDeliveriesBundleList, xBundle, aDeliveryPreparer, aDeliveriesBundlePreparer, 
      aWideIde, aInstalledDeliveriesBundleList, aDeliveriesBundleInstaller, aDelivery, 
      lib, aWT_SequenceTypeExtension, aSequenceType
   
   var BundleCandidate : aEntity
   var Cat : aPreparedDeliveriesBundleList
   var DeliveryRank : Int4
   var CandidateRank : Int4
   var Delivery : aDeliveryPreparer
   var Bundle : aDeliveriesBundlePreparer
   var Found : Boolean
   var line : CString
   var theIDE : aWideIde
   var instCat : aInstalledDeliveriesBundleList
   var instBundle : aDeliveriesBundleInstaller
   var delBundle : aDeliveriesBundle
   var instDel : aDelivery
   var _delivery : tDelivery
   
   ;theIDE = self.GetIde
   BundleCandidate = xBundle.GetBundleCandidateOf(entity)
   if BundleCandidate <> Nil
      Cat = xBundle.GetPreparedbundleCatalog
      if Cat <> Nil
         forEach Bundle in Cat.DelBPreparers
            DeliveryRank = Bundle.FindEntity(BundleCandidate, CandidateRank)
            if DeliveryRank >= 0
               Found = True
               Delivery = Bundle.OwnedDeliveries.GetObjectAt(DeliveryRank)
               _delivery.delivery = Delivery.Name
               _delivery.bundle = Bundle.Name
               lib.SequenceType.Append(_delivery, _Result, _Result.type)
               ;str(line, entity.Name, ' is in prepared (B.D): ', Bundle.Name, '.', 
               ;   Delivery.Name)
               ; theIDE.AppendWideComment(line, GeneralWideComment, True)
            endIf
         endFor
      endIf
      if not Found
         ; search in installed bundles
         BundleCandidate = xBundle.ConfigOwnerOf(entity)
         if BundleCandidate <> Nil
            instCat = xBundle.GetInstalledBundleCatalog
            forEach instBundle in instCat.DelBInstallers
               delBundle = instBundle.alreadyInstalledDelB
               DeliveryRank = FindEntityInDeliveriesBundle(delBundle, BundleCandidate, 
                  CandidateRank)
               if DeliveryRank >= 0
                  Found = True
                  instDel = delBundle.OwnedDeliveries.GetObjectAt(DeliveryRank)
                  _delivery.delivery = instDel.Name
                  _delivery.bundle = delBundle.Name
                  lib.SequenceType.Append(_delivery, _Result, _Result.type)
                  ;str(line, entity.Name, ' is in installed (B.D): ', delBundle.Name, 
                  ;   '.', instDel.Name)
                  ;theIDE.AppendWideComment(line, GeneralWideComment, True)
               endIf
            endFor
         else
            ;  theIDE.AppendWideComment('No candidate for ' + entity.Name, GeneralWideComment, 
            ;     True)
         endIf
      endIf
      if not Found
         ;theIDE.AppendWideComment(entity.Name + ' is NOT in any BUNDLE', GeneralWideComment, 
         ;   True)
      endIf
   else
      ;theIDE.AppendWideComment('No candidate for ' + entity.Name, GeneralWideComment, 
      ;   True)
   endIf
endFunc 

procedure SaveToFile(entity : aEntity)
   uses aWexClassAndModuleExtract, Risky, wUtil
   
   var extractor : aWexClassAndModuleExtract
   var deliveries : tDeliveries
   var curDummyTool : aWexClassAndModuleExtract
   var directory : CString
   
   new(curDummyTool)
   curDummyTool = Risky.ThingFromName(curDummyTool.NameNameSpaceId, cNameForPersistentMainTool, 
      CurrentVersion)
   deliveries = _SearchInBundles(entity)
   directory = curDummyTool.RootDirectory
   if length(deliveries) > 0
      directory += '\' + deliveries[0].bundle + '\' + deliveries[0].delivery
   endIf
   curDummyTool = curDummyTool.NewVersion
   ;
   wUtil.CreateDirsIfNecessary(directory + '\')
   ;
   curDummyTool.SaveEntityToFile(directory, entity)
   curDummyTool.CancelObject(curDummyTool)
   ;
   ;   new(extractor)
   ;   extractor.SaveEntityToFile('', entity)
   ;   dispose(extractor)
endProc 

procedure _WhereUsedReference(myMMViewer : aEntityMMViewer, theUIAgent : aUIAgent)
   uses aLocalConfig, aWideIde, aWideContext, aWAMContainer, aListOfInstances, aListIterator, 
      aGauge, aInstanceVarDesc, aMMBrowser
   
   var theLocalConfig : aLocalConfig
   var curEntity : aEntity
   var ClassNumber : Int4
   var ModuleNumber : Int4
   var SharableObjectsNumber : Int4
   var tmpList : aListOfInstances
   var theIDE : aWideIde
   var curDomain : aWAMContainer
   var maxLaps : Int4
   var it : aListIterator
   var OldTitle : CString
   var WhereUsedCount : Int4
   var i : Int4
   var OldInDefs : Boolean
   var OldInImplems : Boolean
   var OldInScenarios : Boolean
   var OldInSharableObjects : Boolean
   
   if myMMViewer.SearchingWhereUsed
      myMMViewer.SearchingWhereUsed = False
   else
      theIDE = myMMViewer.GetIde
      myMMViewer.gauge.SetTo(0)
      myMMViewer.gauge.UIRefresh
      myMMViewer.WhereUsed.DeleteAllObjects
      myMMViewer.TmpWhereUsed.DeleteAllObjects
      myMMViewer.UIRefreshVar(myMMViewer.TmpWhereUsed)
      myMMViewer.ShowVariableOrMethod(MetaModelEntity(myMMViewer.TmpWhereUsed), True)
      myMMViewer.ShowVariableOrMethod(MetaModelEntity(myMMViewer.WhereUsed), False)
      if theUIAgent <> Nil
         OldTitle = theUIAgent.GetTitle
         theUIAgent.SetTitle('Stop')
      endIf
      myMMViewer.SearchingWhereUsed = True
      if myMMViewer.InDef or myMMViewer.InImplem or myMMViewer.InScenarios or myMMViewer.InSharableObjects
         OldInDefs = myMMViewer.InDef
         OldInImplems = myMMViewer.InImplem
         OldInScenarios = myMMViewer.InScenarios
         OldInSharableObjects = myMMViewer.InSharableObjects
         if myMMViewer.MMBrowser <> Nil
            if myMMViewer.MMBrowser.Domains.count = 0
               theLocalConfig = theIDE.myContext.theLocalConfig
               ClassNumber = theLocalConfig.allClasses.count
               ModuleNumber = theLocalConfig.allModules.count
               if OldInSharableObjects
                  SharableObjectsNumber = theLocalConfig.allOthers.count
               endIf
               myMMViewer.gauge.SetMaxTo(ClassNumber + ModuleNumber + SharableObjectsNumber)
               ;
               myMMViewer.InSharableObjects = False
               it = theLocalConfig.allClasses.NewIterator
               while it.moveNext and myMMViewer.SearchingWhereUsed
                  WhereUsedCount = myMMViewer.WhereUsed.count
                  myMMViewer.WhereUsedReferenceOf(it)
                  myMMViewer.gauge.inc(1)
                  if myMMViewer.WhereUsed.count <> WhereUsedCount
                     for i = WhereUsedCount to myMMViewer.WhereUsed.count - 1
                        curEntity = myMMViewer.WhereUsed.GetObjectAt(i)
                        myMMViewer.TmpWhereUsed.AppendInexistingObject(curEntity.GetEntityAsWhereUsed)
                     endFor
                     myMMViewer.UIRefreshVar(myMMViewer.TmpWhereUsed)
                  endIf
                  if theUIAgent <> Nil
                     theUIAgent.ProcessMessages
                  endIf
               endWhile
               it.Kill(it)
               ;
               it = theLocalConfig.allModules.NewIterator
               while it.moveNext and myMMViewer.SearchingWhereUsed
                  WhereUsedCount = myMMViewer.WhereUsed.count
                  myMMViewer.WhereUsedReferenceOf(it)
                  myMMViewer.gauge.inc(1)
                  if myMMViewer.WhereUsed.count <> WhereUsedCount
                     for i = WhereUsedCount to myMMViewer.WhereUsed.count - 1
                        curEntity = myMMViewer.WhereUsed.GetObjectAt(i)
                        myMMViewer.TmpWhereUsed.AppendInexistingObject(curEntity.GetEntityAsWhereUsed)
                     endFor
                     myMMViewer.UIRefreshVar(myMMViewer.TmpWhereUsed)
                  endIf
                  if theUIAgent <> Nil
                     theUIAgent.ProcessMessages
                  endIf
               endWhile
               it.Kill(it)
               ;
               if OldInSharableObjects
                  myMMViewer.InScenarios = False
                  myMMViewer.InDef = False
                  myMMViewer.InImplem = False
                  myMMViewer.InSharableObjects = True
                  it = theLocalConfig.allOthers.NewIterator
                  while it.moveNext and myMMViewer.SearchingWhereUsed
                     WhereUsedCount = myMMViewer.WhereUsed.count
                     myMMViewer.WhereUsedReferenceOf(it)
                     myMMViewer.gauge.inc(1)
                     if myMMViewer.WhereUsed.count <> WhereUsedCount
                        for i = WhereUsedCount to myMMViewer.WhereUsed.count - 1
                           curEntity = myMMViewer.WhereUsed.GetObjectAt(i)
                           myMMViewer.TmpWhereUsed.AppendInexistingObject(curEntity.GetEntityAsWhereUsed)
                        endFor
                        myMMViewer.UIRefreshVar(myMMViewer.TmpWhereUsed)
                     endIf
                     if theUIAgent <> Nil
                        theUIAgent.ProcessMessages
                     endIf
                  endWhile
                  it.Kill(it)
                  myMMViewer.InScenarios = OldInScenarios
                  myMMViewer.InDef = OldInDefs
                  myMMViewer.InImplem = OldInImplems
               endIf
            else
               forEach curDomain in myMMViewer.MMBrowser.Domains
                  maxLaps += curDomain.Contents.count
               endFor
               myMMViewer.gauge.SetMaxTo(maxLaps)
               forEach curDomain in myMMViewer.MMBrowser.Domains
                  it = curDomain.Contents.NewIterator
                  while it.moveNext and myMMViewer.SearchingWhereUsed
                     WhereUsedCount = myMMViewer.WhereUsed.count
                     myMMViewer.WhereUsedReferenceOf(it)
                     myMMViewer.gauge.inc(1)
                     if myMMViewer.WhereUsed.count <> WhereUsedCount
                        for i = WhereUsedCount to myMMViewer.WhereUsed.count - 1
                           curEntity = myMMViewer.WhereUsed.GetObjectAt(i)
                           myMMViewer.TmpWhereUsed.AppendInexistingObject(curEntity.GetEntityAsWhereUsed)
                        endFor
                        myMMViewer.UIRefreshVar(myMMViewer.TmpWhereUsed)
                     endIf
                     if theUIAgent <> Nil
                        theUIAgent.ProcessMessages
                     endIf
                  endWhile
                  it.Kill(it)
               endFor
            endIf
         endIf
      endIf
      ;i must now filter entities found :
      new(tmpList)
      tmpList.Init
      forEach curEntity in myMMViewer.WhereUsed
         tmpList.AppendInexistingObject(curEntity.GetEntityAsWhereUsed)
      endFor
      myMMViewer.WhereUsed.DeleteAllObjects
      forEach curEntity in tmpList
         myMMViewer.WhereUsed.AppendObject(curEntity)
      endFor
      dispose(tmpList)
      myMMViewer.number = myMMViewer.WhereUsed.count
      myMMViewer.UIRefreshVar(myMMViewer.WhereUsed)
      if theUIAgent <> Nil
         theUIAgent.SetTitle(OldTitle)
      endIf
      myMMViewer.SearchingWhereUsed = False
      myMMViewer.ShowVariableOrMethod(MetaModelEntity(myMMViewer.WhereUsed), True)
      myMMViewer.ShowVariableOrMethod(MetaModelEntity(myMMViewer.TmpWhereUsed), False)
   endIf
endProc 

function WhereUsed(entity : aEntity) return tEntities
   uses aClassDef, lib, aWT_SequenceTypeExtension, aSequenceType, aWT_MMNode, aWT_HttpModule, 
      aWT_HttpServerRouter, aWT_UrlSettings, aMMBrowser
   
   var myMMViewer : aEntityMMViewer
   var MMResponse : tEntity
   var node : aWT_MMNode
   var result : aEntity
   var myMMBrowser : aMMBrowser
   
   if entity <> Nil
      new(myMMViewer)
      new(myMMBrowser)
      myMMViewer.Entity = entity
      myMMViewer.MMBrowser = myMMBrowser
      _WhereUsedReference(myMMViewer, Nil)
      forEach result in myMMViewer.WhereUsed
         MMResponse.name = result.Name
         MMResponse.theType = result.ClassDef.Name
         new(node)
         node.VarAddress = @result
         node.VarType = result.type
         if lib.http <> Nil
            lib.http.Router.Settings.GetNodeURL(MMResponse.location, node)
         endIf
         dispose(node)
         lib.SequenceType.Append(MMResponse, _Result, _Result.type)
      endFor
   endIf
endFunc 

