from functools import lru_cache

from fastapi import FastAPI
from fastapi.openapi import docs
from fastapi.staticfiles import StaticFiles

from api.v1.routes.api import router as api_router
from core.config import get_config
from core.exceptions.heandlers import register_heandlers


@lru_cache()
def get_application() -> FastAPI:
    project_name = get_config().project_name
    debug = get_config().debug
    version = get_config().version
    prefix = get_config().api_prefix
    docs_url = get_config().docs_url
    openapi_url = get_config().openapi_url

    application = FastAPI(
        title=project_name,
        debug=debug,
        version=version,
        docs_url=None,
        redoc_url=None,
        openapi_url=openapi_url,
    )

    application.mount(
        '/static', StaticFiles(directory='static'), name='static'
    )

    @application.get(docs_url, include_in_schema=False)
    def custom_swagger_ui_html():
        return docs.get_swagger_ui_html(
            openapi_url=application.openapi_url,
            title=application.title + ' - Swagger UI',
            oauth2_redirect_url=application.swagger_ui_oauth2_redirect_url,
            swagger_js_url='/static/swagger-ui-bundle.js',
            swagger_css_url='/static/swagger-ui.css',
        )

    @application.get(
        application.swagger_ui_oauth2_redirect_url, 
        include_in_schema=False
    )
    def swagger_ui_redirect():
        return docs.get_swagger_ui_oauth2_redirect_html()

    application.include_router(api_router, prefix=prefix)

    register_heandlers(application)
    
    return application
