from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.api.routers import items_router
from app.api.routers import api_router
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

from logger import logger

# Create the FastAPI application instance
app = FastAPI(docs_url=None, redoc_url=None)

# Include the endpoint routes
app.include_router(api_router)


app.mount(
    "/static", StaticFiles(directory="static"), name="static"
)  # server local js/css for the schema, etc.


# customize openapi
def custom_openapi():
    """create a custom logo"""
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Email API",
        version=1.0,
        description="Auto-email manager.",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {"url": "/static/data-api.png"}
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """serve the static files for swagger inside the cloud"""
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
        swagger_favicon_url="",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    """customized oauth2, required for the static issues inside the cloud"""
    return get_swagger_ui_oauth2_redirect_html()


# custom route for redoc
@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    """serve the static files for redoc inside the cloud"""
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
        redoc_favicon_url="",
        with_google_fonts=False,
    )


# add exception handler to app. this will log errors if there are bad or missing values
# in the headers. i.e. didn't pass a required value
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    logger.error(f"{exc_str} -- {request.url}")
    content = {'status': 'ERROR', 'message': exc_str, 'data': None}
    return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
