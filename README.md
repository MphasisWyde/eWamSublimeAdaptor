# eWamSublimeAdaptor

![front end screen shot](screenshot.png)

## SublimeText "Gold plugin" source code.
Be advised, for now this code is a prototype, a draft. Hence, you will spot some ugly code, some code that's here only for testing purpose, a bunch of commented code lines, clumsy design and lots of debug output in the console. Work in progress.

## Installation
### eWam install
1. Install eWam 6.1.5.0, available on Z:\Wyde Product\eWam & Related Products\Installations 6.1.5 ALPHA\eWAM 6.1.5.0 & Related Products
2. Install eWamExtended (latest version), available on Z:\Wyde Development\eWamExtensions\eWamExtensionsInstallations\eWamExtended Products\wAddOns\eWamAdvancedFramework
3. Add the 2 files in the bin folder
3. Open eWam and create the 2 classes in eWamCode and the JSON module
4. Close eWam
5. Run eWam as a service (you can see it with the process explorer)

### Sublime install
The subfolder SublimeCode/ contains the source code (essentially python) used in the SublimeText package for eWAM Plugin

If you want to use these files "as is", say for testing (i.e. without packaging it in a clean .sublime-package file), you must copy those files directly in the folder (not in a subfolder!) "<user folder>/AppData/Roaming/Sublime Text 3/Packages/User/", where <user folder> is usualy something like C:\Users\username\.

## Features

### Syntax highlighting

The syntax highlighting is defined in the file gold.tmLanguage. It is an XML file in the textmate format (kind of a standard for syntax highlighing definitions, also used by other editors, like VSCode for instance).

This file _could_ be edited directly, **but is more easily generated from a more human readable file : gold.YAML-tmLanguage**. How ? Follow the SublimeText (unofficial) documentation steps: http://docs.sublimetext.info/en/latest/extensibility/syntaxdefs.html

### Menus

...are defined and associated to a command in the Main.sublime-menu file.

Commands are defined in python files (see http://docs.sublimetext.info/en/latest/extensibility/plugins.html) by implementing a class inheriting from one of those classes: sublime_plugin.TextCommand, sublime_plugin.WindowCommand, sublime_plugin.ApplicationCommand, depending on your needs.

### Python source code

... extensively uses SublimeText API (http://www.sublimetext.com/docs/3/api_reference.html).
