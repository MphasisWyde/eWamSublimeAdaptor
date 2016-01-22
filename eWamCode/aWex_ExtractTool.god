;aWex_ExtractTool

class aWex_ExtractTool (aWT_RestResource) 

uses aWexClassAndModuleExtract, aWexConfigurationsToolsExtension, aERS_MMBrowserAPI, 
   aWT_MMNode, aWT_UrlDecorationServerRouter

type tGenerateParam : record
   path : CString
   entities : tEntities
endRecord


;method GET
function Get return tGenerateParam
   uses Risky, aWAMContainer, aClassDef, aWT_UrlDecorationSettings, lib, aWT_SequenceTypeExtension, 
      aSequenceType
   
   var curDummyTool : aWexClassAndModuleExtract
   var entity : aWAMContainer
   var mmresponse : tEntity
   var node : aWT_MMNode
   
   new(curDummyTool)
   curDummyTool = Risky.ThingFromName(curDummyTool.NameNameSpaceId, cNameForPersistentMainTool, 
      CurrentVersion)
   if curDummyTool <> Nil
      _Result.path = curDummyTool.RootDirectory
      forEach entity in curDummyTool.EntitiesToSaveToFile
         mmresponse.name = entity.Name
         mmresponse.theType = entity.ClassDef.Name
         new(node)
         node.VarAddress = @entity
         node.VarType = entity.type
         self.Router.Settings.GetNodeURL(mmresponse.location, node)
         dispose(node)
         lib.SequenceType.Append(mmresponse, _Result.entities, _Result.entities.type)
      endFor
   endIf
endFunc 

;method POST
procedure GenerateSource(body : tGenerateParam)
   uses Risky
   
   var curDummyTool : aWexClassAndModuleExtract
   
   new(curDummyTool)
   curDummyTool = Risky.ThingFromName(curDummyTool.NameNameSpaceId, cNameForPersistentMainTool, 
      CurrentVersion)
   if curDummyTool <> Nil
      curDummyTool = curDummyTool.NewVersion
      if body.path <> ''
         curDummyTool.RootDirectory = body.path
      endIf
      curDummyTool.ActionSaveToFiles(Nil)
      curDummyTool.CancelObject(curDummyTool)
   endIf
endProc 

