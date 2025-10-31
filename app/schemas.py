from enum import Enum
from pydantic import BaseModel, Field, model_validator
from typing import Any, Dict, List, Optional, Union

class TextPart(BaseModel):
    kind: str = Field("text", const=True)
    text: str
    metadata: Optional[Dict[str, Any]] = None

Part = TextPart

class Message(BaseModel):
    role: str
    parts: List[Part]
    extensions: Optional[List[str]] = None
    referenceTaskIds: Optional[List[str]] = None
    taskId: Optional[str] = None
    contextId: Optional[str] = None
    kind: str = "message"
    messageId: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class JSONRPCRequest(BaseModel):
    jsonrpc: str = Field("2.0", const=True)
    method: str
    params: Optional[Dict[str, Any]] = None
    id: Optional[Union[int, str]] = None

    @model_validator
    def check_method(cls, values):
        method = values.get("method")
        if not method or not isinstance(method, str):
            raise ValueError("`method` must be a non-empty string")
        return values
    
class JSONRPCError(BaseModel):
    code: int
    message: str
    data: Optional[Any] = None

class JSONRPCResponse(BaseModel):
    jsonrpc: str = Field("2.0", const=True)
    id: Optional[Union[int, str]]
    result: Optional[Any] = None
    error: Optional[JSONRPCError] = None