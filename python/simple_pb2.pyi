from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChannelType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BUG: _ClassVar[ChannelType]
    SIMPLE: _ClassVar[ChannelType]
    MULTIPLE: _ClassVar[ChannelType]
BUG: ChannelType
SIMPLE: ChannelType
MULTIPLE: ChannelType

class CreateChannelRequest(_message.Message):
    __slots__ = ("name", "type")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: ChannelType
    def __init__(self, name: _Optional[str] = ..., type: _Optional[_Union[ChannelType, str]] = ...) -> None: ...

class CreateChannelResponse(_message.Message):
    __slots__ = ("success", "operation_status_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    OPERATION_STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    operation_status_message: str
    def __init__(self, success: bool = ..., operation_status_message: _Optional[str] = ...) -> None: ...

class RemoveChannelRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class RemoveChannelResponse(_message.Message):
    __slots__ = ("success", "operation_status_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    OPERATION_STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    operation_status_message: str
    def __init__(self, success: bool = ..., operation_status_message: _Optional[str] = ...) -> None: ...

class ListChannelsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListChannelsResponse(_message.Message):
    __slots__ = ("channels",)
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    channels: _containers.RepeatedCompositeFieldContainer[ChannelInfo]
    def __init__(self, channels: _Optional[_Iterable[_Union[ChannelInfo, _Mapping]]] = ...) -> None: ...

class ChannelInfo(_message.Message):
    __slots__ = ("name", "type", "pendingMessages")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PENDINGMESSAGES_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: ChannelType
    pendingMessages: int
    def __init__(self, name: _Optional[str] = ..., type: _Optional[_Union[ChannelType, str]] = ..., pendingMessages: _Optional[int] = ...) -> None: ...

class PublishMessageRequest(_message.Message):
    __slots__ = ("channel", "message")
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    channel: str
    message: _containers.RepeatedCompositeFieldContainer[Message]
    def __init__(self, channel: _Optional[str] = ..., message: _Optional[_Iterable[_Union[Message, _Mapping]]] = ...) -> None: ...

class PublishMessageResponse(_message.Message):
    __slots__ = ("success", "operation_status_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    OPERATION_STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    operation_status_message: str
    def __init__(self, success: bool = ..., operation_status_message: _Optional[str] = ...) -> None: ...

class SubscribeChannelRequest(_message.Message):
    __slots__ = ("channel", "timeout")
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    channel: str
    timeout: int
    def __init__(self, channel: _Optional[str] = ..., timeout: _Optional[int] = ...) -> None: ...

class ReceiveMessageRequest(_message.Message):
    __slots__ = ("channel", "timeout")
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    channel: str
    timeout: int
    def __init__(self, channel: _Optional[str] = ..., timeout: _Optional[int] = ...) -> None: ...

class Message(_message.Message):
    __slots__ = ("content",)
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    content: str
    def __init__(self, content: _Optional[str] = ...) -> None: ...

class ChannelsList(_message.Message):
    __slots__ = ("channels",)
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    channels: _containers.RepeatedCompositeFieldContainer[Channel]
    def __init__(self, channels: _Optional[_Iterable[_Union[Channel, _Mapping]]] = ...) -> None: ...

class Channel(_message.Message):
    __slots__ = ("name", "type", "messages")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: ChannelType
    messages: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., type: _Optional[_Union[ChannelType, str]] = ..., messages: _Optional[_Iterable[str]] = ...) -> None: ...
