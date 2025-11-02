import logging
import traceback

from fastapi import FastAPI, Path, Request
from fastapi.responses import FileResponse, JSONResponse

from app.errors import A2AErrorCode, create_error_response
from .routes import router


logger = logging.getLogger("etymo")
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Etymo - A2A Etymology Agent")

app.include_router(router)

@app.get("/.well-known/agent.json")
async def agent_card():
    path = Path(__file__).resolve().parent / "agent.json"
    if not path.exists():
        return JSONResponse(status_code=404, content={"error": "agent.json not found"})
    return FileResponse(path)

site_dir = Path(__file__).resolve().parent.parent / "site"
if site_dir.exists():
    from fastapi.staticfiles import StaticFiles
    app.mount("/docs", StaticFiles(directory=str(site_dir), html=True), name="docs")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception: %s", exc)
    try:
        body = await request.json()
        req_id = body.get("id")
    except Exception:
        req_id = None
    err = create_error_response(req_id, A2AErrorCode.INTERNAL_ERROR, "Internal error", {"detail": str(exc), "trace": traceback.format_exc()})
    return JSONResponse(status_code=200, content=err)