import logging

from fastapi import APIRouter, Request
from pydantic import ValidationError

from app.errors import A2AErrorCode, create_error_response
from app.schemas import JSONRPCRequest
from app.service import get_etymology
from app.utils import extract_first_text_from_message_parts, make_rpc_result_message


logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/")
async def rpc_entry(request: Request):
    try:
        payload = await request.json()
    except Exception as exc:
        logger.exception("Failed to parse JSON body")
        return create_error_response(None, A2AErrorCode.PARSE_ERROR, "Parse error", {"detail": str(exc)})

    try:
        rpc_req = JSONRPCRequest.model_validate(payload)
    except ValidationError as ve:
        logger.debug("Invalid JSON-RPC request: %s", ve)
        req_id = payload.get("id", None)
        return create_error_response(req_id, A2AErrorCode.INVALID_REQUEST, "Invalid Request", {"errors": ve.errors()})

    request_id = rpc_req.id

    if rpc_req.method == "message/send":
        params = rpc_req.params or {}
        message = params.get("message")
        if not message:
            return create_error_response(request_id, A2AErrorCode.INVALID_PARAMS, "Missing 'message' in params")
        text = extract_first_text_from_message_parts(message)
        if not text:
            return create_error_response(request_id, A2AErrorCode.INVALID_PARAMS, "message.parts must include a text part")
        try:
            ety = await get_etymology(text)
        except Exception as exc:
            logger.exception("Unhandled error in get_etymology")
            return create_error_response(request_id, A2AErrorCode.INTERNAL_ERROR, "Internal error", {"detail": str(exc)})
        result_msg = make_rpc_result_message(ety)
        return {"jsonrpc": "2.0", "id": request_id, "result": result_msg}
    else:
        return create_error_response(request_id, A2AErrorCode.METHOD_NOT_FOUND, "Method not found")