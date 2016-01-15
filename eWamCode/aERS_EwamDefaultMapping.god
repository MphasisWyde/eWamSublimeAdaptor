;aERS_EwamDefaultMapping

class aERS_EwamDefaultMapping (aWT_DefaultUrlMappingSettings) 

uses aWT_HttpRoot, aMethodDesc


procedure ReInit override
   uses aERS_DocumentationAPI, aERS_ModuleDefAPI, aERS_MMBrowserAPI, aERS_EntityAPI
   
   ; self.MapIncomingUrl('*/api/rest/obj/{Object}', [c_GET], MetaModelEntity(aWT_GenericInstanceAPI.GetObject))
   ;
   self.MapIncomingUrl('*/api/rest/documentation', [c_GET], MetaModelEntity(aERS_DocumentationAPI.GetSwaggerDocumentation))
   ;
   ;
   self.MapIncomingUrl('*/api/rest/classOrModule/', [c_PUT], MetaModelEntity(aERS_ModuleDefAPI.Create))
   self.MapIncomingUrl('*/api/rest/classOrModule/{name}', [c_GET], MetaModelEntity(aERS_ModuleDefAPI.Get))
   ;
   ; self.MapOutgoingUrl('*/api/rest/classOrModule/{name}', MetaModelEntity(aERS_ModuleDefAPI.GetOutgoingURLMapping))
   self.MapOutgoingUrl('*/api/rest/classOrModule/{name}', MetaModelEntity(aERS_ModuleDefAPI.GetOutgoingURLMappingForCUImplem))
   ;
   self.MapIncomingUrl('*/api/rest/classOrModule/{name}/descendants', [c_GET], MetaModelEntity(aERS_ModuleDefAPI.GetDescendants))
   self.MapIncomingUrl('*/api/rest/classOrModule/{name}', [c_POST], MetaModelEntity(aERS_ModuleDefAPI.Modify))
   self.MapIncomingUrl('*/api/rest/classOrModule/{name}/CheckOut', [c_POST], MetaModelEntity(aERS_ModuleDefAPI.CheckOut))
   self.MapIncomingUrl('*/api/rest/classOrModule/{name}/CheckIn', [c_POST], MetaModelEntity(aERS_ModuleDefAPI.CheckIn))
   self.MapIncomingUrl('*/api/rest/classOrModule/{name}/scenarios', [c_GET], MetaModelEntity(aERS_ModuleDefAPI.GetScenarios))
   self.MapIncomingUrl('*/api/rest/classOrModule/{name}/entityStatus', [c_GET], MetaModelEntity(aERS_ModuleDefAPI.entityStatus))
   ;
   self.MapIncomingUrl('*/api/rest/classOrModule/{name}/scenarios/{scenarioName}', 
      [c_GET], MetaModelEntity(aERS_ModuleDefAPI.GetMyScenario))
   self.MapOutgoingUrl('*/api/rest/classOrModule/{name}/scenarios/{scenarioName}', 
      MetaModelEntity(aERS_ModuleDefAPI.GetOutgoingURLMappingForScenario))
   ;
   self.MapOutgoingUrl('*/api/rest/entity/{ownerName}/{name}', MetaModelEntity(aERS_EntityAPI.GetOutgoingURLMapping))
   self.MapIncomingUrl('*/api/rest/entity/{ownerName}/{name}', [c_GET], MetaModelEntity(aERS_EntityAPI.GetEntity))
   self.MapIncomingUrl('*/api/rest/entity/{ownerName}/{name}/interact', [c_GET], 
      MetaModelEntity(aERS_EntityAPI.GetEntity))
   ;
   ; self.MapIncomingUrl('*/api/ewam/applicationDescs', [c_GET], MetaModelEntity(aRS_aWFApplicationDesc.Gets))
   ;
   ;  self.MapIncomingUrl('*/api/ewam/bundle/list', [c_GET], MetaModelEntity(aBundleAPI.GetBundles))
   ;
   self.MapIncomingUrl('*/api/rest/searchEntities', [c_GET], MetaModelEntity(aERS_MMBrowserAPI.searchEntities))
endProc 

