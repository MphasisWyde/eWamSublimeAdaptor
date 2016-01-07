; JSON(Def Version:4) (Implem Version:4)

module JSON

uses aFullObject, aWT_JsonValue, aWT_JsonObj, aLightObject, aType


;JSON
function Stringify(object : aLightObject) return Text
   uses aWT_JsonSerializer, aClassDef
   
   var serializer : aWT_JsonSerializer
   
   if object <> Nil
      new(serializer)
      if serializer.Serialize(_Result, @object, object.type)
      endIf
      dispose(serializer)
   endIf
endFunc 

function StringifyEx(VarAddress : Pointer, VarType : aType) return Text
   uses aWT_JsonSerializer
   
   var serializer : aWT_JsonSerializer
   
   new(serializer)
   if serializer.Serialize(_Result, VarAddress, VarType)
   endIf
   dispose(serializer)
endFunc 

function Parse(input : Text) return aWT_JsonValue
   uses aWT_JsonParser
   
   var parser : aWT_JsonParser
   
   new(parser)
   _Result = parser.Parse(input)
   dispose(parser)
endFunc 

function Deserialize(inOut input : Text, object : aFullObject) return Boolean
   uses aWT_JsonSerializer, aClassDef
   
   var serializer : aWT_JsonSerializer
   
   if object <> Nil
      new(serializer)
      _Result = serializer.Deserialize(input, @object, object.type)
      dispose(serializer)
   endIf
endFunc 

function GetJsonValueByRank(body : Text, jpath : CString, rank : Int4) return aWT_JsonValue
   uses lib, aWT_SequenceTypeExtension
   
   var values : tJsonValues
   var parsedBody : aWT_JsonValue
   
   parsedBody = Parse(body)
   if parsedBody <> Nil
      values = parsedBody.JPath(jpath)
      if lib.SequenceType.Len(values) > rank
         _Result = values[rank]
      endIf
   endIf
endFunc 

function GetJsonValue(body : Text, jpath : CString) return aWT_JsonValue
   _Result = GetJsonValueByRank(body, jpath, 0)
endFunc 

function ValueByKeyAsInt(body : Text, key : CString) return Int4
   var value : aWT_JsonValue
   
   value = GetJsonValueByRank(body, key, 0)
   if value <> Nil
      _Result = value.asInt4
   endIf
endFunc 

function ValueByKeyAsBoolean(body : Text, key : CString) return Boolean
   var value : aWT_JsonValue
   
   value = GetJsonValueByRank(body, key, 0)
   if value <> Nil
      _Result = value.asBoolean
   endIf
endFunc 

function ValueByKey(body : Text, key : CString) return CString
   var value : aWT_JsonValue
   
   value = GetJsonValueByRank(body, key, 0)
   if value <> Nil
      _Result = value.asCString
   endIf
endFunc 
