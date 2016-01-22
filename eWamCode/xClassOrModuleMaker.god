;xClassOrModuleMaker

module xClassOrModuleMaker

uses aClassDef, aModuleDef


function CreateClassOrModuleWithText(ParentClass : aClassDef, ClassName : CString, 
   ClassText : Text, inOut ClassToGenerate : aModuleDef, SimulateGeneration : Boolean) return Boolean
   uses wClassOrModuleMaker, Motor
   
   var AllowIt : Boolean
   
   if (ParentClass <> Nil) and (ClassName <> '')
      if SimulateGeneration
         ClassToGenerate = Motor.FindModuleOrClassFromName(ClassName)
         _Result = ClassToGenerate <> Nil
      else
         ClassToGenerate = wClassOrModuleMaker.GetNewOrExistingBlanKClass(ClassName, 
            ParentClass, True, False)
         if ClassToGenerate <> Nil
            wClassOrModuleMaker.AcceptAndRegisterClassOrModule(ClassToGenerate)
            ;
            ClassToGenerate = wClassOrModuleMaker.ProjectOfClassOrModuleFromName(ClassName)
            wClassOrModuleMaker.AddGoldText(ClassToGenerate, ClassText)
            ;FA 07/10/2013 [WPR1310012860]	Allow to generate all classes as private classes
            if not wClassOrModuleMaker.Parse(ClassToGenerate) and (wClassOrModuleMaker.UIModalModifyProject(ClassToGenerate) <> 
               rValid)
               ;NotifyClassParseError(ClassToGenerate, '')
               wClassOrModuleMaker.CancelClassOrModule(ClassToGenerate)
               ;GeneratorError(_ModuleName, _MethodName, Concat('Cannot create class ', 
               ;   ClassName), MajorError)
            else
               ;NotifyClassParseAndBeforeStored(ClassToGenerate, 'set class text, parse and store class')
               ;FA 07/10/2013 [WPR1310012860]	Allow to generate all classes as private classes
               ; GenerateClassWithText is called to generate Servlet,WSDL,XSD,Wrapper,Business classes
               ; if (CurrentWIGeneratorProject <> Nil) and CurrentWIGeneratorProject.GenerateClassAsPrivate
               ;    ClassToGenerate.Modifiers = [clmPrivate]
               ; endIf
               wClassOrModuleMaker.AcceptAndRegisterClassOrModule(ClassToGenerate)
               _Result = True
            endIf
            ;FA 07/10/2013 [WPR1310012860]	Allow to generate all classes as private classes
            ;if (CurrentWIGeneratorProject <> Nil) and CurrentWIGeneratorProject.GenerateClassAsPrivate
            ;   AllowIt = SetAllowAccessToPrivateAndProtectedMembers(AllowIt)
            ;endIf
         else
            ; GeneratorError(_ModuleName, _MethodName, Concat('Cannot create class ', 
            ;    ClassName), MajorError)
         endIf
      endIf
   endIf
endFunc 

