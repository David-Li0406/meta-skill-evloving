/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { ArrayType, BlobType, BooleanType, DateTimeType, DictType, type EastType, FloatType, FunctionType, IntegerType, NullType, RefType, SetType, StringType, StructType, VariantType } from "./types.js";
import { DateTimeFormatTokenType } from "./datetime_format/types.js";

/** @internal */
export type BuiltinType = {
  type_parameters: string[],
  inputs: (string | EastType)[],
  output: string | EastType,
}

/** @internal */
export type BuiltinName = "Is" | "Equal" | "NotEqual" | "Less" | "LessEqual" | "Greater" | "GreaterEqual"
  | "Diff" | "ApplyPatch" | "ComposePatch" | "InvertPatch"
  | "BooleanNot" | "BooleanOr" | "BooleanAnd" | "BooleanXor"
  | "IntegerToFloat" | "IntegerNegate" | "IntegerAdd" | "IntegerSubtract" | "IntegerMultiply" | "IntegerDivide" | "IntegerRemainder" | "IntegerPow" | "IntegerAbs" | "IntegerSign" | "IntegerLog"
  | "FloatToInteger" | "FloatNegate" | "FloatAdd" | "FloatSubtract" | "FloatMultiply" | "FloatDivide" | "FloatRemainder" | "FloatPow" | "FloatAbs" | "FloatSign" | "FloatSqrt" | "FloatExp" | "FloatLog" | "FloatSin" | "FloatCos" | "FloatTan"
  | "Print" | "Parse" | "StringConcat" | "StringRepeat" | "StringLength" | "StringSubstring" | "StringUpperCase" | "StringLowerCase" | "StringSplit" | "StringTrim" | "StringTrimStart" | "StringTrimEnd" | "StringStartsWith" | "StringEndsWith" | "StringContains" | "StringIndexOf" | "StringReplace" | "RegexContains" | "RegexIndexOf" | "RegexReplace" | "StringEncodeUtf8" | "StringEncodeUtf16" | "StringParseJSON" | "StringPrintJSON"
  | "DateTimeGetYear" | "DateTimeGetMonth" | "DateTimeGetDayOfMonth" | "DateTimeGetHour" | "DateTimeGetMinute" | "DateTimeGetSecond" | "DateTimeGetDayOfWeek" | "DateTimeGetMillisecond" | "DateTimeAddMilliseconds" | "DateTimeDurationMilliseconds" | "DateTimeToEpochMilliseconds" | "DateTimeFromEpochMilliseconds" | "DateTimeFromComponents" | "DateTimePrintFormat" | "DateTimeParseFormat"
  | "BlobSize" | "BlobGetUint8" | "BlobDecodeUtf8" | "BlobDecodeUtf16" | "BlobDecodeBeast" | "BlobEncodeBeast" | "BlobDecodeBeast2" | "BlobEncodeBeast2" | "BlobDecodeCsv" | "ArrayEncodeCsv"
  | "RefGet" | "RefUpdate" | "RefMerge"
  | "ArrayGenerate" | "ArrayRange" | "ArrayLinspace" | "ArraySize" | "ArrayHas" | "ArrayGet" | "ArrayGetOrDefault" | "ArrayTryGet" | "ArrayUpdate" | "ArrayMerge" | "ArrayPushLast" | "ArrayPopLast" | "ArrayPushFirst" | "ArrayPopFirst" | "ArrayAppend" | "ArrayPrepend" | "ArrayMergeAll" | "ArrayClear" | "ArraySortInPlace" | "ArrayReverseInPlace" | "ArraySort" | "ArrayReverse" | "ArrayIsSorted" | "ArrayFindSortedFirst" | "ArrayFindSortedLast" | "ArrayFindSortedRange" | "ArrayFindFirst" | "ArrayConcat" | "ArraySlice" | "ArrayGetKeys" | "ArrayForEach" | "ArrayCopy" | "ArrayMap" | "ArrayFilter" | "ArrayFilterMap" | "ArrayFirstMap" | "ArrayMapReduce" | "ArrayFold" | "ArrayStringJoin" | "ArrayToSet" | "ArrayToDict" | "ArrayFlattenToArray" | "ArrayFlattenToSet" | "ArrayFlattenToDict" | "ArrayGroupFold"
  | "SetGenerate" | "SetSize" | "SetHas" | "SetInsert" | "SetTryInsert" | "SetDelete" | "SetTryDelete" | "SetClear" | "SetUnionInPlace" | "SetUnion" | "SetIntersect" | "SetDiff" | "SetSymDiff" | "SetIsSubset" | "SetIsDisjoint" | "SetCopy" | "SetForEach" | "SetMap" | "SetFilter" | "SetFilterMap" | "SetFirstMap" | "SetMapReduce" | "SetReduce" | "SetToArray" | "SetToSet" |"SetToDict" | "SetFlattenToArray" | "SetFlattenToSet" | "SetFlattenToDict" | "SetGroupFold"
  | "DictGenerate" | "DictSize" | "DictHas" | "DictGet" | "DictGetOrDefault" | "DictTryGet" | "DictInsert" | "DictGetOrInsert" | "DictInsertOrUpdate" | "DictUpdate" | "DictSwap" | "DictMerge" | "DictDelete" | "DictTryDelete" | "DictPop" | "DictClear" | "DictUnionInPlace" | "DictMergeAll" | "DictKeys" | "DictGetKeys" | "DictForEach" | "DictCopy" | "DictMap" | "DictFilter" | "DictFilterMap" | "DictFirstMap" | "DictMapReduce" | "DictReduce" | "DictToArray" | "DictToSet" | "DictToDict" | "DictFlattenToArray" | "DictFlattenToSet" | "DictFlattenToDict" | "DictGroupFold"
  ;

/** @internal */
export const Builtins: Record<BuiltinName, BuiltinType> = {
  Is: {
    type_parameters: ["T"],
    inputs: ["T", "T"] as const,
    output: BooleanType,
  },
  Equal: {
    type_parameters: ["T"],
    inputs: ["T", "T"] as const,
    output: BooleanType,
  },
  NotEqual: {
    type_parameters: ["T"],
    inputs: ["T", "T"] as const,
    output: BooleanType,
  },
  Less: {
    type_parameters: ["T"],
    inputs: ["T", "T"] as const,
    output: BooleanType,
  },
  LessEqual: {
    type_parameters: ["T"],
    inputs: ["T", "T"] as const,
    output: BooleanType,
  },
  Greater: {
    type_parameters: ["T"],
    inputs: ["T", "T"] as const,
    output: BooleanType,
  },
  GreaterEqual: {
    type_parameters: ["T"],
    inputs: ["T", "T"] as const,
    output: BooleanType,
  },
  // Patch operations - P is the computed PatchType passed from expression building
  // We use two type parameters because the patch type structure varies based on T
  Diff: {
    type_parameters: ["T", "P"],
    inputs: ["T", "T"] as const,
    output: "P",
  },
  ApplyPatch: {
    type_parameters: ["T", "P"],
    inputs: ["T", "P"] as const,
    output: "T",
  },
  ComposePatch: {
    type_parameters: ["T", "P"],
    inputs: ["P", "P"] as const,
    output: "P",
  },
  InvertPatch: {
    type_parameters: ["T", "P"],
    inputs: ["P"] as const,
    output: "P",
  },
  BooleanNot: {
    type_parameters: [],
    inputs: [BooleanType] as const,
    output: BooleanType,
  },
  BooleanOr: {
    type_parameters: [],
    inputs: [BooleanType, BooleanType] as const,
    output: BooleanType,
  },
  BooleanAnd: {
    type_parameters: [],
    inputs: [BooleanType, BooleanType] as const,
    output: BooleanType,
  },
  BooleanXor: {
    type_parameters: [],
    inputs: [BooleanType, BooleanType] as const,
    output: BooleanType,
  },

  IntegerToFloat: {
    type_parameters: [],
    inputs: [IntegerType] as const,
    output: FloatType,
  },
  IntegerNegate: {
    type_parameters: [],
    inputs: [IntegerType] as const,
    output: IntegerType,
  },
  IntegerAdd: {
    type_parameters: [],
    inputs: [IntegerType, IntegerType] as const,
    output: IntegerType,
  },
  IntegerSubtract: {
    type_parameters: [],
    inputs: [IntegerType, IntegerType] as const,
    output: IntegerType,
  },
  IntegerMultiply: {
    type_parameters: [],
    inputs: [IntegerType, IntegerType] as const,
    output: IntegerType,
  },
  IntegerDivide: { // TODO add rounding mode
    type_parameters: [],
    inputs: [IntegerType, IntegerType] as const,
    output: IntegerType,
  },
  IntegerRemainder: { // TODO add rounding mode
    type_parameters: [],
    inputs: [IntegerType, IntegerType] as const,
    output: IntegerType,
  },
  IntegerPow: {
    type_parameters: [],
    inputs: [IntegerType, IntegerType] as const,
    output: IntegerType,
  },
  IntegerAbs: {
    type_parameters: [],
    inputs: [IntegerType] as const,
    output: IntegerType,
  },
  IntegerSign: {
    type_parameters: [],
    inputs: [IntegerType] as const,
    output: IntegerType,
  },
  IntegerLog: {
    type_parameters: [],
    inputs: [IntegerType, IntegerType] as const,
    output: IntegerType,
  },

  FloatToInteger: {
    type_parameters: [],
    inputs: [FloatType] as const,
    output: IntegerType,
  },
  FloatNegate: {
    type_parameters: [],
    inputs: [FloatType] as const,
    output: FloatType,
  },
  FloatAdd: {
    type_parameters: [],
    inputs: [FloatType, FloatType] as const,
    output: FloatType,
  },
  FloatSubtract: {
    type_parameters: [],
    inputs: [FloatType, FloatType] as const,
    output: FloatType,
  },
  FloatMultiply: {
    type_parameters: [],
    inputs: [FloatType, FloatType] as const,
    output: FloatType,
  },
  FloatDivide: { // TODO add rounding mode
    type_parameters: [],
    inputs: [FloatType, FloatType] as const,
    output: FloatType,
  },
  FloatRemainder: { // TODO add rounding mode
    type_parameters: [],
    inputs: [FloatType, FloatType] as const,
    output: FloatType,
  },
  FloatPow: {
    type_parameters: [],
    inputs: [FloatType, FloatType] as const,
    output: FloatType,
  },
  FloatAbs: {
    type_parameters: [],
    inputs: [FloatType] as const,
    output: FloatType,
  },
  FloatSign: {
    type_parameters: [],
    inputs: [FloatType] as const,
    output: FloatType,
  },
  FloatSqrt: {
    type_parameters: [],
    inputs: [FloatType] as const,
    output: FloatType,
  },
  FloatExp: {
    type_parameters: [],
    inputs: [FloatType] as const,
    output: FloatType,
  },
  FloatLog: {
    type_parameters: [],
    inputs: [FloatType] as const,
    output: FloatType,
  },
  FloatSin: {
    type_parameters: [],
    inputs: [FloatType] as const,
    output: FloatType,
  },
  FloatCos: {
    type_parameters: [],
    inputs: [FloatType] as const,
    output: FloatType,
  },
  FloatTan: {
    type_parameters: [],
    inputs: [FloatType] as const,
    output: FloatType,
  },

  StringConcat: {
    type_parameters: [],
    inputs: [StringType, StringType] as const,
    output: StringType,
  },
  StringRepeat: {
    type_parameters: [],
    inputs: [StringType, IntegerType] as const,
    output: StringType,
  },
  StringLength: {
    type_parameters: [],
    inputs: [StringType] as const,
    output: IntegerType,
  },
  StringSubstring: {
    type_parameters: [],
    inputs: [StringType, IntegerType, IntegerType] as const,
    output: StringType,
  },
  StringUpperCase: {
    type_parameters: [],
    inputs: [StringType] as const,
    output: StringType,
  },
  StringLowerCase: {
    type_parameters: [],
    inputs: [StringType] as const,
    output: StringType,
  },
  StringSplit: {
    type_parameters: [],
    inputs: [StringType, StringType] as const,
    output: ArrayType(StringType),
  },
  StringTrim: {
    type_parameters: [],
    inputs: [StringType] as const,
    output: StringType,
  },
  StringTrimStart: {
    type_parameters: [],
    inputs: [StringType] as const,
    output: StringType,
  },
  StringTrimEnd: {
    type_parameters: [],
    inputs: [StringType] as const,
    output: StringType,
  },
  StringStartsWith: {
    type_parameters: [],
    inputs: [StringType, StringType] as const,
    output: BooleanType,
  },
  StringEndsWith: {
    type_parameters: [],
    inputs: [StringType, StringType] as const,
    output: BooleanType,
  },
  StringContains: {
    type_parameters: [],
    inputs: [StringType, StringType] as const,
    output: BooleanType,
  },
  StringIndexOf: {
    type_parameters: [],
    inputs: [StringType, StringType] as const,
    output: IntegerType,
  },
  StringReplace: {
    type_parameters: [],
    inputs: [StringType, StringType, StringType] as const,
    output: StringType,
  },
  RegexContains: {
    type_parameters: [],
    inputs: [StringType, StringType, StringType] as const,
    output: BooleanType,
  },
  RegexIndexOf: {
    type_parameters: [],
    inputs: [StringType, StringType, StringType] as const,
    output: IntegerType,
  },
  RegexReplace: {
    type_parameters: [],
    inputs: [StringType, StringType, StringType, StringType] as const,
    output: StringType,
  },
  StringEncodeUtf8: {
    type_parameters: [],
    inputs: [StringType] as const,
    output: BlobType,
  },
  StringEncodeUtf16: {
    type_parameters: [],
    inputs: [StringType] as const,
    output: BlobType,
  },
  Print: {
    type_parameters: ["T"],
    inputs: ["T"] as const,
    output: StringType,
  },
  Parse: {
    type_parameters: ["T"],
    inputs: [StringType] as const,
    output: "T",
  },
  StringPrintJSON: {
    type_parameters: ["T"],
    inputs: ["T"] as const,
    output: StringType,
  },
  StringParseJSON: {
    type_parameters: ["T"],
    inputs: [StringType] as const,
    output: "T",
  },

  DateTimeGetYear: {
    type_parameters: [],
    inputs: [DateTimeType] as const,
    output: IntegerType,
  },
  DateTimeGetMonth: {
    type_parameters: [],
    inputs: [DateTimeType] as const,
    output: IntegerType,
  },
  DateTimeGetDayOfMonth: {
    type_parameters: [],
    inputs: [DateTimeType] as const,
    output: IntegerType,
  },
  DateTimeGetHour: {
    type_parameters: [],
    inputs: [DateTimeType] as const,
    output: IntegerType,
  },
  DateTimeGetMinute: {
    type_parameters: [],
    inputs: [DateTimeType] as const,
    output: IntegerType,
  },
  DateTimeGetSecond: {
    type_parameters: [],
    inputs: [DateTimeType] as const,
    output: IntegerType,
  },
  DateTimeGetMillisecond: {
    type_parameters: [],
    inputs: [DateTimeType] as const,
    output: IntegerType,
  },
  DateTimeGetDayOfWeek: {
    type_parameters: [],
    inputs: [DateTimeType] as const,
    output: IntegerType,
  },
  DateTimeToEpochMilliseconds: {
    type_parameters: [],
    inputs: [DateTimeType] as const,
    output: IntegerType,
  },
  DateTimeFromEpochMilliseconds: {
    type_parameters: [],
    inputs: [IntegerType] as const,
    output: DateTimeType,
  },
  DateTimeFromComponents: {
    type_parameters: [],
    inputs: [IntegerType, IntegerType, IntegerType, IntegerType, IntegerType, IntegerType, IntegerType] as const,
    output: DateTimeType,
  },
  DateTimeAddMilliseconds: {
    type_parameters: [],
    inputs: [DateTimeType, IntegerType] as const,
    output: DateTimeType,
  },
  DateTimeDurationMilliseconds: {
    type_parameters: [],
    inputs: [DateTimeType, DateTimeType] as const,
    output: IntegerType,
  },
  DateTimePrintFormat: {
    type_parameters: [],
    inputs: [DateTimeType, ArrayType(DateTimeFormatTokenType)] as const,
    output: StringType,
  },
  DateTimeParseFormat: {
    type_parameters: [],
    inputs: [StringType, ArrayType(DateTimeFormatTokenType)] as const,
    output: DateTimeType,
  },

  BlobSize: {
    type_parameters: [],
    inputs: [BlobType] as const,
    output: IntegerType,
  },
  BlobGetUint8: {
    type_parameters: [],
    inputs: [BlobType, IntegerType] as const,
    output: IntegerType,
  },
  BlobDecodeUtf8: {
    type_parameters: [],
    inputs: [BlobType] as const,
    output: StringType,
  },
  BlobDecodeUtf16: {
    type_parameters: [],
    inputs: [BlobType] as const,
    output: StringType,
  },
  BlobDecodeBeast: {
    type_parameters: ["T"],
    inputs: [BlobType] as const,
    output: "T",
  },
  BlobEncodeBeast: {
    type_parameters: ["T"],
    inputs: ["T"] as const,
    output: BlobType,
  },
  BlobDecodeBeast2: {
    type_parameters: ["T"],
    inputs: [BlobType] as const,
    output: "T",
  },
  BlobEncodeBeast2: {
    type_parameters: ["T"],
    inputs: ["T"] as const,
    output: BlobType,
  },
  BlobDecodeCsv: {
    type_parameters: ["T", "Config"],
    inputs: [BlobType, "Config"] as const,
    output: ArrayType("T"),
  },
  ArrayEncodeCsv: {
    type_parameters: ["T", "Config"],
    inputs: [ArrayType("T"), "Config"] as const,
    output: BlobType,
  },

  RefGet: {
    type_parameters: ["T"],
    inputs: [RefType("T")] as const,
    output: "T",
  },
  RefUpdate: {
    type_parameters: ["T"],
    inputs: [RefType("T"), "T"] as const,
    output: NullType,
  },
  RefMerge: {
    type_parameters: ["T", "T2"],
    inputs: [RefType("T"), "T2", FunctionType(["T", "T2"], "T")] as const,
    output: NullType,
  },

  ArrayGenerate: {
    type_parameters: ["T"],
    inputs: [IntegerType, FunctionType([IntegerType], "T")] as const,
    output: ArrayType("T"),
  },
  ArrayRange: {
    type_parameters: [],
    inputs: [IntegerType, IntegerType, IntegerType] as const,
    output: ArrayType(IntegerType),
  },
  ArrayLinspace: {
    type_parameters: [],
    inputs: [FloatType, FloatType, IntegerType] as const,
    output: ArrayType(FloatType),
  },
  ArraySize: {
    type_parameters: ["T"],
    inputs: [ArrayType("T")] as const,
    output: IntegerType,
  },
  ArrayHas: {
    type_parameters: ["T"],
    inputs: [ArrayType("T"), IntegerType] as const,
    output: BooleanType,
  },
  ArrayGet: {
    type_parameters: ["T"],
    inputs: [ArrayType("T"), IntegerType] as const,
    output: "T",
  },
  ArrayGetOrDefault: {
    type_parameters: ["T"],
    inputs: [ArrayType("T"), IntegerType, FunctionType([IntegerType], "T")] as const,
    output: "T",
  },
  ArrayTryGet: {
    type_parameters: ["T"],
    inputs: [ArrayType("T"), IntegerType] as const,
    output: VariantType({ none: NullType, some: "T" }),
  },
  ArrayUpdate: {
    type_parameters: ["T"],
    inputs: [ArrayType("T"), IntegerType, "T"] as const,
    output: NullType,
  },
  ArrayMerge: {
    type_parameters: ["T", "T2"],
    inputs: [ArrayType("T"), IntegerType, "T2", FunctionType(["T", "T2", IntegerType], "T")] as const,
    output: NullType,
  },
  ArrayPushLast: {
    type_parameters: ["T"],
    inputs: [ArrayType("T"), "T"] as const,
    output: NullType,
  },
  ArrayPopLast: {
    type_parameters: ["T"],
    inputs: [ArrayType("T")] as const,
    output: "T",
  },
  ArrayPushFirst: {
    type_parameters: ["T"],
    inputs: [ArrayType("T"), "T"] as const,
    output: NullType,
  },
  ArrayPopFirst: {
    type_parameters: ["T"],
    inputs: [ArrayType("T")] as const,
    output: "T",
  },
  ArrayAppend: {
    type_parameters: ["T"],
    inputs: [ArrayType("T"), ArrayType("T")] as const,
    output: NullType,
  },
  ArrayPrepend: {
    type_parameters: ["T"],
    inputs: [ArrayType("T"), ArrayType("T")] as const,
    output: NullType,
  },
  ArrayMergeAll: {
    type_parameters: ["T", "T2"],
    inputs: [ArrayType("T"), ArrayType("T2"), FunctionType(["T", "T2", IntegerType], "T")] as const,
    output: NullType,
  },
  ArrayClear: {
    type_parameters: ["T"],
    inputs: [ArrayType("T")] as const,
    output: NullType,
  },
  ArraySortInPlace: {
    type_parameters: ["T", "T2"],
    inputs: [ArrayType("T"), FunctionType(["T"], "T2")] as const,
    output: NullType,
  },
  ArrayReverseInPlace: {
    type_parameters: ["T"],
    inputs: [ArrayType("T")] as const,
    output: NullType,
  },
  ArraySort: {
    type_parameters: ["T", "T2"],
    inputs: [ArrayType("T"), FunctionType(["T"], "T2")] as const,
    output: ArrayType("T"),
  },
  ArrayReverse: {
    type_parameters: ["T"],
    inputs: [ArrayType("T")] as const,
    output: ArrayType("T"),
  },
  ArrayIsSorted: {
    type_parameters: ["T", "T2"],
    inputs: [ArrayType("T"), FunctionType(["T"], "T2")] as const,
    output: BooleanType,
  },
  ArrayFindSortedFirst: {
    type_parameters: ["T", "T2"],
    inputs: [ArrayType("T"), "T2", FunctionType(["T"], "T2")] as const,
    output: IntegerType,
  },
  ArrayFindSortedLast: {
    type_parameters: ["T", "T2"],
    inputs: [ArrayType("T"), "T2", FunctionType(["T"], "T2")] as const,
    output: IntegerType,
  },
  ArrayFindSortedRange: {
    type_parameters: ["T", "T2"],
    inputs: [ArrayType("T"), "T2", FunctionType(["T"], "T2")] as const,
    output: StructType({ start: IntegerType, end: IntegerType }),
  },
  ArrayFindFirst: {
    type_parameters: ["T", "T2"],
    inputs: [ArrayType("T"), "T2", FunctionType(["T"], "T2")] as const,
    output: VariantType({ none: NullType, some: IntegerType }),
  },
  ArrayConcat: {
    type_parameters: ["T"],
    inputs: [ArrayType("T"), ArrayType("T")] as const,
    output: ArrayType("T"),
  },
  ArraySlice: {
    type_parameters: ["T"],
    inputs: [ArrayType("T"), IntegerType, IntegerType] as const,
    output: ArrayType("T"),
  },
  ArrayGetKeys: {
    type_parameters: ["T"],
    inputs: [ArrayType("T"), ArrayType(IntegerType), FunctionType([IntegerType], "T")] as const,
    output: ArrayType("T"),
  },
  ArrayForEach: {
    type_parameters: ["T", "T2"],
    inputs: [ArrayType("T"), FunctionType(["T", IntegerType], "T2")] as const,
    output: NullType,
  },
  ArrayCopy: {
    type_parameters: ["T"],
    inputs: [ArrayType("T")] as const,
    output: ArrayType("T"),
  },
  ArrayMap: {
    type_parameters: ["T", "T2"],
    inputs: [ArrayType("T"), FunctionType(["T", IntegerType], "T2")] as const,
    output: ArrayType("T2"),
  },
  ArrayFilter: {
    type_parameters: ["T"],
    inputs: [ArrayType("T"), FunctionType(["T", IntegerType], BooleanType)] as const,
    output: ArrayType("T"),
  },
  ArrayFilterMap: {
    type_parameters: ["T", "T2"],
    inputs: [ArrayType("T"), FunctionType(["T", IntegerType], VariantType({ none: NullType, some: "T2" }))] as const,
    output: ArrayType("T2"),
  },
  ArrayFirstMap: {
    type_parameters: ["T", "T2"],
    inputs: [ArrayType("T"), FunctionType(["T", IntegerType], VariantType({ none: NullType, some: "T2" }))] as const,
    output: VariantType({ none: NullType, some: "T2" }),
  },
  ArrayFold: {
    type_parameters: ["T", "T2"],
    inputs: [ArrayType("T"), "T2", FunctionType(["T2", "T", IntegerType], "T2")] as const,
    output: "T2",
  },
  ArrayMapReduce: {
    type_parameters: ["T", "T2"],
    inputs: [ArrayType("T"), FunctionType(["T", IntegerType], "T2"), FunctionType(["T2", "T2"], "T2")] as const,
    output: "T2",
  },
  ArrayStringJoin: {
    type_parameters: [],
    inputs: [ArrayType(StringType), StringType] as const,
    output: StringType,
  },
  ArrayToSet: {
    type_parameters: ["T", "K2"],
    inputs: [ArrayType("T"), FunctionType(["T", IntegerType], "K2")] as const,
    output: SetType("K2"),
  },
  ArrayToDict: {
    type_parameters: ["T", "K2", "T2"],
    inputs: [ArrayType("T"), FunctionType(["T", IntegerType], "K2"), FunctionType(["T", IntegerType], "T2"), FunctionType(["T2", "T2", "K2"], "T2")] as const,
    output: DictType("K2", "T2"),
  },
  ArrayFlattenToArray: {
    type_parameters: ["T", "T2"],
    inputs: [ArrayType("T"), FunctionType(["T", IntegerType], ArrayType("T2"))] as const,
    output: ArrayType("T2"),
  },
  ArrayFlattenToSet: {
    type_parameters: ["T", "K2"],
    inputs: [ArrayType("T"), FunctionType(["T", IntegerType], SetType("K2"))] as const,
    output: SetType("K2"),
  },
  ArrayFlattenToDict: {
    type_parameters: ["T", "K2", "T2"],
    inputs: [ArrayType("T"), FunctionType(["T", IntegerType], DictType("K2", "T2")), FunctionType(["T2", "T2", "K2"], "T2")] as const,
    output: DictType("K2", "T2"),
  },
  ArrayGroupFold: {
    type_parameters: ["T", "K2", "T2"],
    inputs: [ArrayType("T"), FunctionType(["T", IntegerType], "K2"), FunctionType(["K2"], "T2"), FunctionType(["T2", "T", IntegerType], "T2")] as const,
    output: DictType("K2", "T2"),
  },

  SetGenerate: {
    type_parameters: ["K"],
    inputs: [IntegerType, FunctionType([IntegerType], "K"), FunctionType(["K"], NullType)] as const,
    output: SetType("K"),
  },
  SetSize: {
    type_parameters: ["K"],
    inputs: [SetType("K")] as const,
    output: IntegerType,
  },
  SetHas: {
    type_parameters: ["K"],
    inputs: [SetType("K"), "K"] as const,
    output: BooleanType,
  },
  SetInsert: {
    type_parameters: ["K"],
    inputs: [SetType("K"), "K"] as const,
    output: NullType,
  },
  SetTryInsert: {
    type_parameters: ["K"],
    inputs: [SetType("K"), "K"] as const,
    output: BooleanType,
  },
  SetDelete: {
    type_parameters: ["K"],
    inputs: [SetType("K"), "K"] as const,
    output: NullType,
  },
  SetTryDelete: {
    type_parameters: ["K"],
    inputs: [SetType("K"), "K"] as const,
    output: BooleanType,
  },
  SetUnionInPlace: {
    type_parameters: ["K"],
    inputs: [SetType("K"), SetType("K")] as const,
    output: NullType,
  },
  SetClear: {
    type_parameters: ["K"],
    inputs: [SetType("K")] as const,
    output: NullType,
  },
  SetUnion: {
    type_parameters: ["K"],
    inputs: [SetType("K"), SetType("K")] as const,
    output: SetType("K"),
  },
  SetIntersect: {
    type_parameters: ["K"],
    inputs: [SetType("K"), SetType("K")] as const,
    output: SetType("K"),
  },
  SetDiff: {
    type_parameters: ["K"],
    inputs: [SetType("K"), SetType("K")] as const,
    output: SetType("K"),
  },
  SetSymDiff: {
    type_parameters: ["K"],
    inputs: [SetType("K"), SetType("K")] as const,
    output: SetType("K"),
  },
  SetIsSubset: {
    type_parameters: ["K"],
    inputs: [SetType("K"), SetType("K")] as const,
    output: BooleanType,
  },
  SetIsDisjoint: {
    type_parameters: ["K"],
    inputs: [SetType("K"), SetType("K")] as const,
    output: BooleanType,
  },
  SetCopy: {
    type_parameters: ["K"],
    inputs: [SetType("K")] as const,
    output: SetType("K"),
  },
  SetForEach: {
    type_parameters: ["K", "T2"],
    inputs: [SetType("K"), FunctionType(["K"], "T2")] as const,
    output: NullType,
  },
  SetMap: {
    type_parameters: ["K", "T2"],
    inputs: [SetType("K"), FunctionType(["K"], "T2")] as const,
    output: DictType("K", "T2"),
  },
  SetFilter: {
    type_parameters: ["K"],
    inputs: [SetType("K"), FunctionType(["K"], BooleanType)] as const,
    output: SetType("K"),
  },
  SetFilterMap: {
    type_parameters: ["K", "V2"],
    inputs: [SetType("K"), FunctionType(["K"], VariantType({ none: NullType, some: "V2" }))] as const,
    output: DictType("K", "V2"),
  },
  SetFirstMap: {
    type_parameters: ["K", "T2"],
    inputs: [SetType("K"), FunctionType(["K"], VariantType({ none: NullType, some: "T2" }))] as const,
    output: VariantType({ none: NullType, some: "T2" }),
  },
  SetMapReduce: {
    type_parameters: ["K", "T2"],
    inputs: [SetType("K"), FunctionType(["K"], "T2"), FunctionType(["T2", "T2"], "T2")] as const,
    output: "T2",
  },
  SetReduce: {
    type_parameters: ["K", "T2"],
    inputs: [SetType("K"), FunctionType(["T2", "K"], "T2"), "T2"] as const,
    output: "T2",
  },
  SetToArray: {
    type_parameters: ["K", "T2"],
    inputs: [SetType("K"), FunctionType(["K"], "T2")] as const,
    output: ArrayType("T2"),
  },
  SetToSet: {
    type_parameters: ["K", "K2"],
    inputs: [SetType("K"), FunctionType(["K"], "K2")] as const,
    output: SetType("K2"),
  },
  SetToDict: {
    type_parameters: ["K", "K2", "T2"],
    inputs: [SetType("K"), FunctionType(["K"], "K2"), FunctionType(["K"], "T2"), FunctionType(["T2", "T2", "K2"], "T2")] as const,
    output: DictType("K2", "T2"),
  },
  SetFlattenToArray: {
    type_parameters: ["K", "T2"],
    inputs: [SetType("K"), FunctionType(["K"], ArrayType("T2"))] as const,
    output: ArrayType("T2"),
  },
  SetFlattenToSet: {
    type_parameters: ["K", "K2"],
    inputs: [SetType("K"), FunctionType(["K"], SetType("K2"))] as const,
    output: SetType("K2"),
  },
  SetFlattenToDict: {
    type_parameters: ["K", "K2", "T2"],
    inputs: [SetType("K"), FunctionType(["K"], DictType("K2", "T2")), FunctionType(["T2", "T2", "K2"], "T2")] as const,
    output: DictType("K2", "T2"),
  },
  SetGroupFold: {
    type_parameters: ["K", "K2", "T2"],
    inputs: [SetType("K"), FunctionType(["K"], "K2"), FunctionType(["K2"], "T2"), FunctionType(["T2", "K"], "T2")] as const,
    output: DictType("K2", "T2"),
  },

  DictGenerate: {
    type_parameters: ["K", "V"],
    inputs: [IntegerType, FunctionType([IntegerType], "K"), FunctionType([IntegerType], "V"), FunctionType(["V", "V", "K"], "V")] as const,
    output: DictType("K", "V"),
  },
  DictSize: {
    type_parameters: ["K", "V"],
    inputs: [DictType("K", "V")] as const,
    output: IntegerType,
  },
  DictHas: {
    type_parameters: ["K", "V"],
    inputs: [DictType("K", "V"), "K"] as const,
    output: BooleanType,
  },
  DictGet: {
    type_parameters: ["K", "V"],
    inputs: [DictType("K", "V"), "K"] as const,
    output: "V",
  },
  DictGetOrDefault: {
    type_parameters: ["K", "V"],
    inputs: [DictType("K", "V"), "K", FunctionType(["K"], "V")] as const,
    output: "V",
  },
  DictTryGet: {
    type_parameters: ["K", "V"],
    inputs: [DictType("K", "V"), "K"] as const,
    output: VariantType({ none: NullType, some: "V" }),
  },
  DictInsert: {
    type_parameters: ["K", "V"],
    inputs: [DictType("K", "V"), "K", "V"] as const,
    output: NullType,
  },
  DictInsertOrUpdate: {
    type_parameters: ["K", "V"],
    inputs: [DictType("K", "V"), "K", "V", FunctionType(["V", "V", "K"], "V")] as const,
    output: NullType,
  },
  DictGetOrInsert: {
    type_parameters: ["K", "V"],
    inputs: [DictType("K", "V"), "K", FunctionType(["K"], "V")] as const,
    output: "V",
  },
  DictUpdate: {
    type_parameters: ["K", "V"],
    inputs: [DictType("K", "V"), "K", "V"] as const,
    output: NullType,
  },
  DictSwap: {
    type_parameters: ["K", "V"],
    inputs: [DictType("K", "V"), "K", "V"] as const,
    output: "V",
  },
  DictMerge: {
    type_parameters: ["K", "V", "V2"],
    inputs: [DictType("K", "V"), "K", "V2", FunctionType(["V", "V2", "K"], "V"), FunctionType(["K"], "V")] as const,
    output: NullType,
  },
  DictDelete: {
    type_parameters: ["K", "V"],
    inputs: [DictType("K", "V"), "K"] as const,
    output: NullType,
  },
  DictTryDelete: {
    type_parameters: ["K", "V"],
    inputs: [DictType("K", "V"), "K"] as const,
    output: BooleanType,
  },
  DictPop: {
    type_parameters: ["K", "V"],
    inputs: [DictType("K", "V"), "K"] as const,
    output: "V",
  },
  DictClear: {
    type_parameters: ["K", "V"],
    inputs: [DictType("K", "V")] as const,
    output: NullType,
  },
  DictUnionInPlace: {
    type_parameters: ["K", "V"],
    inputs: [DictType("K", "V"), DictType("K", "V"), FunctionType(["V", "V", "K"], "V")] as const,
    output: NullType,
  },
  DictMergeAll: {
    type_parameters: ["K", "V", "V2"],
    inputs: [DictType("K", "V"), DictType("K", "V2"), FunctionType(["V", "V2", "K"], "V"), FunctionType(["K"], "V")] as const,
    output: NullType,
  },
  DictKeys: {
    type_parameters: ["K", "V"],
    inputs: [DictType("K", "V")] as const,
    output: SetType("K"),
  },
  DictGetKeys: {
    type_parameters: ["K", "V"],
    inputs: [DictType("K", "V"), SetType("K"), FunctionType(["K"], "V")] as const,
    output: DictType("K", "V"),
  },
  DictForEach: {
    type_parameters: ["K", "V", "T2"],
    inputs: [DictType("K", "V"), FunctionType(["V", "K"], "T2")] as const,
    output: NullType,
  },
  DictCopy: {
    type_parameters: ["K", "V"],
    inputs: [DictType("K", "V")] as const,
    output: DictType("K", "V"),
  },
  DictMap: {
    type_parameters: ["K", "V", "V2"],
    inputs: [DictType("K", "V"), FunctionType(["V", "K"], "V2")] as const,
    output: DictType("K", "V2"),
  },
  DictFilter: {
    type_parameters: ["K", "V"],
    inputs: [DictType("K", "V"), FunctionType(["V", "K"], BooleanType)] as const,
    output: DictType("K", "V"),
  },
  DictFilterMap: {
    type_parameters: ["K", "V", "V2"],
    inputs: [DictType("K", "V"), FunctionType(["V", "K"], VariantType({ none: NullType, some: "V2" }))] as const,
    output: DictType("K", "V2"),
  },
  DictFirstMap: {
    type_parameters: ["K", "V", "T2"],
    inputs: [DictType("K", "V"), FunctionType(["V", "K"], VariantType({ none: NullType, some: "T2" }))] as const,
    output: VariantType({ none: NullType, some: "T2" }),
  },
  DictMapReduce: {
    type_parameters: ["K", "V", "T2"],
    inputs: [DictType("K", "V"), FunctionType(["V", "K"], "T2"), FunctionType(["T2", "T2"], "T2")] as const,
    output: "T2",
  },
  DictReduce: {
    type_parameters: ["K", "V", "T2"],
    inputs: [DictType("K", "V"), FunctionType(["T2", "V", "K"], "T2"), "T2"] as const,
    output: "T2",
  },
  DictToArray: {
    type_parameters: ["K", "V", "T2"],
    inputs: [DictType("K", "V"), FunctionType(["V", "K"], "T2")] as const,
    output: ArrayType("T2"),
  },
  DictToSet: {
    type_parameters: ["K", "V", "K2"],
    inputs: [DictType("K", "V"), FunctionType(["V", "K"], "K2")] as const,
    output: SetType("K2"),
  },
  DictToDict: {
    type_parameters: ["K", "V", "K2", "V2"],
    inputs: [DictType("K", "V"), FunctionType(["V", "K"], "K2"), FunctionType(["V", "K"], "V2"), FunctionType(["V2", "V2", "K2"], "V2")] as const,
    output: DictType("K2", "V2"),
  },
  DictFlattenToArray: {
    type_parameters: ["K", "V", "T2"],
    inputs: [DictType("K", "V"), FunctionType(["V", "K"], ArrayType("T2"))] as const,
    output: ArrayType("T2"),
  },
  DictFlattenToSet: {
    type_parameters: ["K", "V", "K2"],
    inputs: [DictType("K", "V"), FunctionType(["V", "K"], SetType("K2"))] as const,
    output: SetType("K2"),
  },
  DictFlattenToDict: {
    type_parameters: ["K", "V", "K2", "V2"],
    inputs: [DictType("K", "V"), FunctionType(["V", "K"], DictType("K2", "V2")), FunctionType(["V2", "V2", "K2"], "V2")] as const,
    output: DictType("K2", "V2"),
  },
  DictGroupFold: {
    type_parameters: ["K", "V", "K2", "T2"],
    inputs: [DictType("K", "V"), FunctionType(["V", "K"], "K2"), FunctionType(["K2"], "T2"), FunctionType(["T2", "V", "K"], "T2")] as const,
    output: DictType("K2", "T2"),
  },
}

/** @internal */
export function applyTypeParameters(type: EastType | string, params: Map<string, EastType>, inStack: EastType[], outStack: EastType[]): EastType {
  const idx = inStack.indexOf(type as EastType);
  if (idx !== -1) {
    return outStack[idx]!;
  }

  if (typeof(type) === "string") {
    let ret = params.get(type);
    if (ret === undefined) {
      throw new Error(`Unable to find type parameter ${JSON.stringify(type)}`);
    }
    return ret;
  } else if (type.type === "Null" || type.type === "Boolean" || type.type === "Integer" || type.type === "Float" || type.type === "String" || type.type === "DateTime" || type.type ==="Blob" || type.type === "Never") {
    return type;
  } else if (type.type === "Ref") {
    const self = { type: "Ref" as const, value: undefined as unknown as EastType };
    inStack.push(type);
    outStack.push(self);
    self.value = applyTypeParameters(type.value, params, inStack, outStack);
    inStack.pop();
    outStack.pop();
    return self;
  } else if (type.type === "Array") {
    const self = { type: "Array" as const, value: undefined as unknown as EastType };
    inStack.push(type);
    outStack.push(self);
    self.value = applyTypeParameters(type.value, params, inStack, outStack);
    inStack.pop();
    outStack.pop();
    return self;
  } else if (type.type === "Set") {
    const self = { type: "Set" as const, key: undefined as unknown as EastType };
    inStack.push(type);
    outStack.push(self);
    self.key = applyTypeParameters(type.key, params, inStack, outStack);
    inStack.pop();
    outStack.pop();
    return self;
  } else if (type.type === "Dict") {
    const self = { type: "Dict" as const, key: undefined as unknown as EastType, value: undefined as unknown as EastType };
    inStack.push(type);
    outStack.push(self);
    self.key = applyTypeParameters(type.key, params, inStack, outStack);
    self.value = applyTypeParameters(type.value, params, inStack, outStack);
    inStack.pop();
    outStack.pop();
    return self;
  } else if (type.type === "Struct") {
    const self = { type: "Struct" as const, fields: {} as Record<string, EastType> };
    inStack.push(type);
    outStack.push(self);
    for (const [name, fieldType] of Object.entries(type.fields)) {
      self.fields[name] = applyTypeParameters(fieldType, params, inStack, outStack);
    }
    inStack.pop();
    outStack.pop();
    return self;
  } else if (type.type === "Variant") {
    const self = { type: "Variant" as const, cases: {} as Record<string, EastType> };
    inStack.push(type);
    outStack.push(self);
    for (const [name, caseType] of Object.entries(type.cases)) {
      self.cases[name] = applyTypeParameters(caseType, params, inStack, outStack);
    }
    inStack.pop();
    outStack.pop();
    return self;
  } else if (type.type === "Recursive") {
    const self = { type: "Recursive" as const, node: undefined as unknown as EastType };
    inStack.push(type);
    outStack.push(self);
    self.node = applyTypeParameters(type.node, params, inStack, outStack);
    inStack.pop();
    outStack.pop();
    return self;
  } else if (type.type === "Function") {
    const self = {
      type: "Function" as const,
      inputs: [] as EastType[],
      output: undefined as unknown as EastType,
    };
    inStack.push(type);
    outStack.push(self);
    for (const inputType of type.inputs) {
      self.inputs.push(applyTypeParameters(inputType, params, inStack, outStack));
    }
    self.output = applyTypeParameters(type.output, params, inStack, outStack);
    inStack.pop();
    outStack.pop();
    return self;
  } else if (type.type === "AsyncFunction") {
    const self = {
      type: "AsyncFunction" as const,
      inputs: [] as EastType[],
      output: undefined as unknown as EastType,
    };
    inStack.push(type);
    outStack.push(self);
    for (const inputType of type.inputs) {
      self.inputs.push(applyTypeParameters(inputType, params, inStack, outStack));
    }
    self.output = applyTypeParameters(type.output, params, inStack, outStack);
    inStack.pop();
    outStack.pop();
    return self;
  } else {
    throw new Error(`Unhandled type ${((type satisfies never) as EastType).type}`)
  }
}
