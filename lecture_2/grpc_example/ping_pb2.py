# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: ping.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'ping.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nping.proto\x12\x0cgrpc_example\"\x1e\n\x0bPingRequest\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x1f\n\x0cPongResponce\x12\x0f\n\x07message\x18\x01 \x01(\t2\x92\x01\n\x08PingPong\x12=\n\x04Ping\x12\x19.grpc_example.PingRequest\x1a\x1a.grpc_example.PongResponce\x12G\n\nPingStream\x12\x19.grpc_example.PingRequest\x1a\x1a.grpc_example.PongResponce(\x01\x30\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ping_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_PINGREQUEST']._serialized_start=28
  _globals['_PINGREQUEST']._serialized_end=58
  _globals['_PONGRESPONCE']._serialized_start=60
  _globals['_PONGRESPONCE']._serialized_end=91
  _globals['_PINGPONG']._serialized_start=94
  _globals['_PINGPONG']._serialized_end=240
# @@protoc_insertion_point(module_scope)
