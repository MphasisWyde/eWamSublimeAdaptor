;aERS_Bundle

class aERS_Bundle (aWT_RestResource) 

type tBundleInfo : record
   file : CString
endRecord


procedure install(body : tBundleInfo)
   uses aInstalledDeliveriesBundleList
   
   var installer : aInstalledDeliveriesBundleList
   
   new(installer)
   if body.file = ''
      installer.pickAFileToInstall
   else
      installer.fileToInstall = body.file
   endIf
   if installer.fileToInstall <> ''
      installer.installAllVersions
   endIf
   dispose(installer)
   ;end
endProc 

