import logging
import time
import jwt
from dataclasses import asdict
from typing import Callable

from fastapi import FastAPI, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic.error_wrappers import ValidationError
from sqlalchemy import URL, text

from fast_api.v1.endpoints import home
from fast_api.v1.populate.populate_db import populate_database
from fast_api.v1.settings import ENGINE, SETTINGS

logger = logging.getLogger(__name__)

description = """
    Sample AirBnB API
    """

app = FastAPI(
    title="AirBnB API Exercise",
    description=description,
    version="v1",
    contact={"name": "Margarita Linets"},
)

COMPONENT_ENDPOINTS = [home.endpoint]


def _configure_routers(component: FastAPI) -> None:
    for endpoint in COMPONENT_ENDPOINTS:
        component.include_router(endpoint.router, prefix=endpoint.prefix)
    return


def _configure_stats(component: FastAPI) -> None:
    # Default middleware configuration to add stats we would want to log
    @component.middleware("http")
    async def add_middleware(request: Request, call_next: Callable) -> Response:
        start = time.time()
        response = await call_next(request)
        process_time = time.time() - start
        response.headers["X-Process-Time"] = str(process_time)
        return response


def _configure_authentication(component: FastAPI) -> None:
    @component.middleware("http")
    async def add_auth_middleware(request: Request, call_next):
        EXCLUDED_PATHS = ["/docs", "/openapi.json"]

        if request["path"] in EXCLUDED_PATHS:
            response = await call_next(request)
            return response

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content="Request missing access token",
            )
        try:
            jwt.decode(
                auth_header.replace("Bearer", "").strip(),
                "secret",
                algorithms=["HS256"],
            )
        except jwt.exceptions.DecodeError:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN, content="Invalid token"
            )
        response = await call_next(request)
        return response


def _configure_middleware(component: FastAPI) -> None:
    # Attaching middlwares defined in settings
    for m in SETTINGS.middlewares:
        logger.info(f"[!] Attaching {m[0].__name__}")
        component.add_middleware(m[0], **m[1])
        logger.info(f"[+] {m[0].__name__} attached")


def _configure_logging(component: FastAPI) -> None:
    pass


def _configure_db(component: FastAPI) -> None:
    with ENGINE.connect() as connection:
        logger.info("[!] Validating database connection")
        connection.execute(text("SELECT 1"))
        logger.warn(f"[+] DB Connection succeeded!")
        logger.warn(f"[!] Trying to populate database")
        status = populate_database()
        logger.warn(f"[+] {status}")


def _configure_validation_error_handler(component: FastAPI) -> None:
    # Adding custom exception handler to intercept pydantic validation errors
    # and return HTTP 422 code
    @component.exception_handler(ValidationError)
    async def handle_exception(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"detail": exc.errors()}),
        )


_configure_stats(app)
_configure_middleware(app)
_configure_routers(app)
_configure_validation_error_handler(app)
_configure_logging(app)
_configure_db(app)
_configure_authentication(app)
