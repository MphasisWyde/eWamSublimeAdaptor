cd..

svn export --force https://github.com/MphasisWyde/ewam-advanced-framework/trunk/WFDll



if not exist Bundle mkdir Bundle
cd bundle
svn export --force https://github.com/MphasisWyde/ewam-advanced-framework/trunk/Bundle/WxWAMAdvancedComponents 


svn export --force https://github.com/MphasisWyde/eWamExtended/trunk/Bundle/WxBundleToolsEx/Bundle/BundleToolsEx