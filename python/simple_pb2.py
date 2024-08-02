# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: simple.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0csimple.proto\x12\nteste_grpc\"K\n\x14\x43reateChannelRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12%\n\x04type\x18\x02 \x01(\x0e\x32\x17.teste_grpc.ChannelType\"J\n\x15\x43reateChannelResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12 \n\x18operation_status_message\x18\x02 \x01(\t\"$\n\x14RemoveChannelRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"J\n\x15RemoveChannelResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12 \n\x18operation_status_message\x18\x02 \x01(\t\"\x15\n\x13ListChannelsRequest\"A\n\x14ListChannelsResponse\x12)\n\x08\x63hannels\x18\x01 \x03(\x0b\x32\x17.teste_grpc.ChannelInfo\"[\n\x0b\x43hannelInfo\x12\x0c\n\x04name\x18\x01 \x01(\t\x12%\n\x04type\x18\x02 \x01(\x0e\x32\x17.teste_grpc.ChannelType\x12\x17\n\x0fpendingMessages\x18\x03 \x01(\x05\"9\n\x15PublishMessageRequest\x12\x0f\n\x07\x63hannel\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\x0c\"K\n\x16PublishMessageResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12 \n\x18operation_status_message\x18\x02 \x01(\t\";\n\x17SubscribeChannelRequest\x12\x0f\n\x07\x63hannel\x18\x01 \x01(\t\x12\x0f\n\x07timeout\x18\x02 \x01(\x05\"9\n\x15ReceiveMessageRequest\x12\x0f\n\x07\x63hannel\x18\x01 \x01(\t\x12\x0f\n\x07timeout\x18\x02 \x01(\x05\"+\n\x07Message\x12\x0f\n\x07\x63hannel\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\t\"4\n\x0bMessageList\x12%\n\x08messages\x18\x01 \x03(\x0b\x32\x13.teste_grpc.Message*\'\n\x0b\x43hannelType\x12\n\n\x06SIMPLE\x10\x00\x12\x0c\n\x08MULTIPLE\x10\x01\x32\x82\x04\n\x0eMessageManager\x12T\n\rCreateChannel\x12 .teste_grpc.CreateChannelRequest\x1a!.teste_grpc.CreateChannelResponse\x12T\n\rRemoveChannel\x12 .teste_grpc.RemoveChannelRequest\x1a!.teste_grpc.RemoveChannelResponse\x12Q\n\x0cListChannels\x12\x1f.teste_grpc.ListChannelsRequest\x1a .teste_grpc.ListChannelsResponse\x12W\n\x0ePublishMessage\x12!.teste_grpc.PublishMessageRequest\x1a\".teste_grpc.PublishMessageResponse\x12N\n\x10SubscribeChannel\x12#.teste_grpc.SubscribeChannelRequest\x1a\x13.teste_grpc.Message0\x01\x12H\n\x0eReceiveMessage\x12!.teste_grpc.ReceiveMessageRequest\x1a\x13.teste_grpc.Messageb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'simple_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CHANNELTYPE']._serialized_start=833
  _globals['_CHANNELTYPE']._serialized_end=872
  _globals['_CREATECHANNELREQUEST']._serialized_start=28
  _globals['_CREATECHANNELREQUEST']._serialized_end=103
  _globals['_CREATECHANNELRESPONSE']._serialized_start=105
  _globals['_CREATECHANNELRESPONSE']._serialized_end=179
  _globals['_REMOVECHANNELREQUEST']._serialized_start=181
  _globals['_REMOVECHANNELREQUEST']._serialized_end=217
  _globals['_REMOVECHANNELRESPONSE']._serialized_start=219
  _globals['_REMOVECHANNELRESPONSE']._serialized_end=293
  _globals['_LISTCHANNELSREQUEST']._serialized_start=295
  _globals['_LISTCHANNELSREQUEST']._serialized_end=316
  _globals['_LISTCHANNELSRESPONSE']._serialized_start=318
  _globals['_LISTCHANNELSRESPONSE']._serialized_end=383
  _globals['_CHANNELINFO']._serialized_start=385
  _globals['_CHANNELINFO']._serialized_end=476
  _globals['_PUBLISHMESSAGEREQUEST']._serialized_start=478
  _globals['_PUBLISHMESSAGEREQUEST']._serialized_end=535
  _globals['_PUBLISHMESSAGERESPONSE']._serialized_start=537
  _globals['_PUBLISHMESSAGERESPONSE']._serialized_end=612
  _globals['_SUBSCRIBECHANNELREQUEST']._serialized_start=614
  _globals['_SUBSCRIBECHANNELREQUEST']._serialized_end=673
  _globals['_RECEIVEMESSAGEREQUEST']._serialized_start=675
  _globals['_RECEIVEMESSAGEREQUEST']._serialized_end=732
  _globals['_MESSAGE']._serialized_start=734
  _globals['_MESSAGE']._serialized_end=777
  _globals['_MESSAGELIST']._serialized_start=779
  _globals['_MESSAGELIST']._serialized_end=831
  _globals['_MESSAGEMANAGER']._serialized_start=875
  _globals['_MESSAGEMANAGER']._serialized_end=1389
# @@protoc_insertion_point(module_scope)
