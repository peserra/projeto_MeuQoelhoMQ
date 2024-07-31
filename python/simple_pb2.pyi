from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RequestOpening(_message.Message):
    __slots__ = ("client_id", "client_name")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_NAME_FIELD_NUMBER: _ClassVar[int]
    client_id: int
    client_name: str
    def __init__(self, client_id: _Optional[int] = ..., client_name: _Optional[str] = ...) -> None: ...

class StatusOpening(_message.Message):
    __slots__ = ("mess",)
    MESS_FIELD_NUMBER: _ClassVar[int]
    mess: str
    def __init__(self, mess: _Optional[str] = ...) -> None: ...
