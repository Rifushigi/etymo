from enum import Enum
from typing import Any, Dict, Optional, Union


class A2AErrorCode(Enum):
    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603

def create_error_response(
        request_id: Optional[Union[str, int]],
        code: A2AErrorCode,
        message: str,
        data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": request_id if request_id is not None else None,
        "error": {
            "code": code.value,
            "message": message,
            "data": data or {},
        },
    }

class A2AException(Exception):
    def __init__(
            self,
            code: A2AErrorCode,
            message: str,
            request_id: Optional[Union[str, int]] = None,
            data: Optional[Dict[str, Any]] = None,
            ):
        super().__init__(message)
        self.message =  message
        self.code = code
        self.request_id = request_id
        self.data = data or {}