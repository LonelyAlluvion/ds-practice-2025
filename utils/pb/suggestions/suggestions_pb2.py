# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: suggestions.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11suggestions.proto\x12\x0bsuggestions\"|\n\x15RecommendationRequest\x12\x10\n\x08order_id\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\t\x12*\n\x0fpurchased_books\x18\x03 \x03(\x0b\x32\x11.suggestions.Book\x12\x14\n\x0cvector_clock\x18\x04 \x03(\x05\"6\n\x04\x42ook\x12\x0f\n\x07\x62ook_id\x18\x01 \x01(\t\x12\r\n\x05title\x18\x02 \x01(\t\x12\x0e\n\x06\x61uthor\x18\x03 \x01(\t\"Z\n\x16RecommendationResponse\x12*\n\x0fsuggested_books\x18\x01 \x03(\x0b\x32\x11.suggestions.Book\x12\x14\n\x0cvector_clock\x18\x02 \x03(\x05\";\n\x11\x43learOrderRequest\x12\x10\n\x08order_id\x18\x01 \x01(\t\x12\x14\n\x0cvector_clock\x18\x02 \x03(\x05\"%\n\x12\x43learOrderResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x32\xbb\x01\n\x0bSuggestions\x12Y\n\x0eRecommendBooks\x12\".suggestions.RecommendationRequest\x1a#.suggestions.RecommendationResponse\x12Q\n\x0e\x43learOrderData\x12\x1e.suggestions.ClearOrderRequest\x1a\x1f.suggestions.ClearOrderResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'suggestions_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_RECOMMENDATIONREQUEST']._serialized_start=34
  _globals['_RECOMMENDATIONREQUEST']._serialized_end=158
  _globals['_BOOK']._serialized_start=160
  _globals['_BOOK']._serialized_end=214
  _globals['_RECOMMENDATIONRESPONSE']._serialized_start=216
  _globals['_RECOMMENDATIONRESPONSE']._serialized_end=306
  _globals['_CLEARORDERREQUEST']._serialized_start=308
  _globals['_CLEARORDERREQUEST']._serialized_end=367
  _globals['_CLEARORDERRESPONSE']._serialized_start=369
  _globals['_CLEARORDERRESPONSE']._serialized_end=406
  _globals['_SUGGESTIONS']._serialized_start=409
  _globals['_SUGGESTIONS']._serialized_end=596
# @@protoc_insertion_point(module_scope)
