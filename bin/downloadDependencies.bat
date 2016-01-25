cd..

svn export --force https://github.com/MphasisWyde/ewam-advanced-framework/trunk/WFDll

svn export --force https://github.com/swagger-api/swagger-ui/trunk/dist

if not exist Bundle mkdir Bundle
cd bundle
svn export --force https://github.com/MphasisWyde/ewam-advanced-framework/trunk/Bundle/WxWAMAdvancedComponents 


svn export --force https://github.com/MphasisWyde/wAddOns/trunk/WxBundleToolsEx/Bundle/BundleToolsEx/

svn export --force https://github.com/MphasisWyde/wAddOns/trunk/WxSelectiveExportManager/Bundle/WxSelectiveExportManager