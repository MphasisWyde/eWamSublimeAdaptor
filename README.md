# eWamSublimeAdaptor

![front end screen shot](screenshot.png)

## SublimeText "Gold plugin" source code.
Be advised, for now this code is a prototype, a draft. Hence, you will spot some ugly code, some code that's here only for testing purpose, a bunch of commented code lines, clumsy design and lots of debug output in the console. Work in progress.

## Installation
### eWam install
* Install eWam 6.1.5.1
  * available on Z:\Wyde Product\eWam & Related Products\Installations 6.1.5 ALPHA\eWAM 6.1.5.0 & Related Products
* Clone this repository and copy its content into your eWamRoot
* Double click on bin/downloaddependencies.bat
* Open eWam
* Install the bundle WXeWamExtended (until version 29)   
* Install the bundle WxSelectiveExportManager (until version 13)  
* Install the bundle WxBundleToolsEx (until version 17)
* Close eWam
* Open eWam
* Use configuration-> Selective Export Manager
  * Select the file %wyde-root%\eWamCode\api.xml
  * Uncheck `Use stationary ids`
  * Click on import
	

### Sublime install
The subfolder SublimeCode/ contains the source code (essentially python) used in the SublimeText package for eWAM Plugin

If you want to use these files "as is", say for testing (i.e. without packaging it in a clean .sublime-package file), you must copy the folder you want (say v0.1_POC_via_REST) in "<user folder>/AppData/Roaming/Sublime Text 3/Packages/", where <user folder> is usualy something like C:\Users\username\.

## Running it 	
* Run eWam as a service (you can see it with the process explorer)
	make sure you run the 
		eWAM - service.bat as administrator.
		The easiest way to do this is to Create a Run as Admin shortcut for your bat file.
			*create a shortcut of eWAM - service.bat, 
			*get properties of the shortcut,
			*click advanced
			*check the run as Admin box.
			*save

## To test this configuration open your web browser to :

	http://localhost:8082/aeWamManager/openentity/aWT_CStringTypeExtension
	this assume you are using the default port 8082.
	To validate the port being used consult the 
	ewam.json fine in the bin folder and validate the line
	url:"http://+:8082/"
	if your 8082 is in use you could try changing the port, 
	recommeded ports are 49152 to 65535

	
## Troubleshooting:

	if you get an this error
	HttpAddUrl failed with 5, 
	the service does not have permission to start
		* make sure you don't have any Windows updates that are installed and waiting for a reboot (often when updates are pending it locks down a number of ports).


### Using your own 6.1 TGV?
You have to first run ewam with the option `/PATCHSYSTEM`


## Features

### Syntax highlighting

The syntax highlighting is defined in the file gold.tmLanguage. It is an XML file in the textmate format (kind of a standard for syntax highlighing definitions, also used by other editors, like VSCode for instance).

This file _could_ be edited directly, **but is more easily generated from a more human readable file : gold.YAML-tmLanguage**. How ? Follow the SublimeText (unofficial) documentation steps: http://docs.sublimetext.info/en/latest/extensibility/syntaxdefs.html

### Menus

...are defined and associated to a command in the Main.sublime-menu file.

Commands are defined in python files (see http://docs.sublimetext.info/en/latest/extensibility/plugins.html) by implementing a class inheriting from one of those classes: sublime_plugin.TextCommand, sublime_plugin.WindowCommand, sublime_plugin.ApplicationCommand, depending on your needs.

### Python source code

... extensively uses SublimeText API (http://www.sublimetext.com/docs/3/api_reference.html).
