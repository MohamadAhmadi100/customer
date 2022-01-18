import uvicorn
from fastapi import FastAPI
from fastapi import responses
from starlette.exceptions import HTTPException as starletteHTTPException

from controllers.router_register import router_register
from controllers.router_auth import router_auth
from controllers.router_profile import router_profile

app = FastAPI(
    debug=True,
    title="Customer",
    version="0.1.0",
    docs_url="/api/v1/docs/"
)
app.include_router(router_register)
app.include_router(router_auth)
app.include_router(router_profile)


@app.exception_handler(starletteHTTPException)
def validation_exception_handler(request, exc):
    return responses.JSONResponse(exc.detail, status_code=exc.status_code)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
