;aERS_EwamDefaultMapping

class aERS_EwamDefaultMapping (aWT_DefaultUrlMappingSettings) 

uses aWT_HttpRoot, aMethodDesc


procedure ReInit override
   uses aERS_DocumentationAPI, aERS_ModuleDefAPI, aERS_MMBrowserAPI, aERS_EntityAPI, 
      aWT_DefaultProcessor, aERS_Repository, aWex_ExtractTool, aERS_Bundle
   
   self.PreProcess('*', c_UNDEF, MetaModelEntity(aWT_DefaultProcessor.AllowCORS))
   ;
   self.MapIncomingUrl('*/api/rest/documentation', [c_GET], MetaModelEntity(aERS_DocumentationAPI.GetSwaggerDocumentation))
   ;
   ;
   self.MapIncomingUrl('*/api/rest/classOrModule/', [c_PUT], MetaModelEntity(aERS_ModuleDefAPI.Create))
   self.MapIncomingUrl('*/api/rest/classOrModule/{name}', [c_GET], MetaModelEntity(aERS_ModuleDefAPI.Get))
   ;
   ;
   self.MapIncomingUrl('*/api/rest/searchEntities', [c_GET], MetaModelEntity(aERS_MMBrowserAPI.searchEntities))
   self.MapOutgoingUrl('*/api/rest/classOrModule/{name}', MetaModelEntity(aERS_ModuleDefAPI.GetOutgoingURLMappingForCUImplem))
   ;   ;
   self.MapIncomingUrl('*/api/rest/classOrModule/{name}/descendants', [c_GET], MetaModelEntity(aERS_ModuleDefAPI.GetDescendants))
   self.MapIncomingUrl('*/api/rest/classOrModule/{name}', [c_POST], MetaModelEntity(aERS_ModuleDefAPI.Modify))
   self.MapIncomingUrl('*/api/rest/classOrModule/{name}/CheckOut', [c_POST], MetaModelEntity(aERS_ModuleDefAPI.CheckOut))
   self.MapIncomingUrl('*/api/rest/classOrModule/{name}/CheckIn', [c_POST], MetaModelEntity(aERS_ModuleDefAPI.CheckIn))
   self.MapIncomingUrl('*/api/rest/classOrModule/{name}/Deliver', [c_POST], MetaModelEntity(aERS_ModuleDefAPI.Deliver))
   self.MapIncomingUrl('*/api/rest/classOrModule/{name}/ManageReimplem', [c_POST, 
      c_GET], MetaModelEntity(aERS_ModuleDefAPI.ManageReimplem))
   self.MapIncomingUrl('*/api/rest/classOrModule/{name}/scenarios', [c_GET], MetaModelEntity(aERS_ModuleDefAPI.GetScenarios))
   self.MapIncomingUrl('*/api/rest/classOrModule/{name}/entityStatus', [c_GET], MetaModelEntity(aERS_ModuleDefAPI.entityStatus))
   self.MapIncomingUrl('*/api/rest/classOrModule/{name}/parse', [c_POST], MetaModelEntity(aERS_ModuleDefAPI.Parse))
   ;   ;
   self.MapIncomingUrl('*/api/rest/classOrModule/{name}/scenarios/{scenarioName}', 
      [c_GET], MetaModelEntity(aERS_ModuleDefAPI.GetMyScenario))
   self.MapOutgoingUrl('*/api/rest/classOrModule/{name}/scenarios/{scenarioName}', 
      MetaModelEntity(aERS_ModuleDefAPI.GetOutgoingURLMappingForScenario))
   ;   ;
   self.MapOutgoingUrl('*/api/rest/entity/{ownerName}/{name}', MetaModelEntity(aERS_EntityAPI.GetOutgoingURLMapping))
   self.MapIncomingUrl('*/api/rest/entity/{ownerName}/{name}', [c_GET], MetaModelEntity(aERS_EntityAPI.GetEntity))
   self.MapIncomingUrl('*/api/rest/entity/{ownerName}/{name}/CheckIn', [c_POST], 
      MetaModelEntity(aERS_EntityAPI.CheckIn))
   self.MapIncomingUrl('*/api/rest/entity/{ownerName}/{name}/CheckOut', [c_POST], 
      MetaModelEntity(aERS_EntityAPI.CheckOut))
   self.MapIncomingUrl('*/api/rest/entity/{ownerName}/{name}/deliver', [c_POST], 
      MetaModelEntity(aERS_EntityAPI.Deliver))
   self.MapIncomingUrl('*/api/rest/entity/{ownerName}/{name}/interact', [c_GET], 
      MetaModelEntity(aERS_EntityAPI.GetEntity))
   self.MapIncomingUrl('*/api/rest/entity/{ownerName}/{name}/whereUsed', [c_GET], 
      MetaModelEntity(aERS_EntityAPI.WhereUsed))
   ;
   self.MapIncomingUrl('*/api/rest/repository/deliver', [c_POST], MetaModelEntity(aERS_Repository.Deliver))
   self.MapIncomingUrl('*/api/rest/repository/deliverAll', [c_POST], MetaModelEntity(aERS_Repository.DeliverAll))
   self.MapIncomingUrl('*/api/rest/repository/checkInAll', [c_POST], MetaModelEntity(aERS_Repository.CheckinAll))
   self.MapIncomingUrl('*/api/rest/repository/synchronize', [c_POST], MetaModelEntity(aERS_Repository.Synchronize))
   self.MapIncomingUrl('*/api/rest/repository/status', [c_GET], MetaModelEntity(aERS_Repository.Status))
   ;
   self.MapIncomingUrl('*/api/rest/extractTool/getSettings', [c_GET], MetaModelEntity(aWex_ExtractTool.Get))
   self.MapIncomingUrl('*/api/rest/extractTool/generatesource', [c_POST], MetaModelEntity(aWex_ExtractTool.GenerateSource))
   ;
   self.MapIncomingUrl('*/api/rest/bundle/install', [c_POST], MetaModelEntity(aERS_Bundle.install))
endProc 

