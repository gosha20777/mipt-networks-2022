from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from core.exceptions.app import AppError, InputError
from core.exceptions.db import DbError


def db_error_handler(request: Request, exc: DbError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={'message': 'Database error!'}
    )


def input_error_handler(request: Request, exc: InputError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={'message': str(exc)}
    )


def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={'message': str(exc)}
    )


def register_heandlers(app: FastAPI):
    app.add_exception_handler(InputError, input_error_handler)
    app.add_exception_handler(DbError, db_error_handler)
    app.add_exception_handler(AppError, app_error_handler)
