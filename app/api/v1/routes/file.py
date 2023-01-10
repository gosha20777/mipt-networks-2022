import logging

from fastapi import APIRouter, File, Query
from fastapi.params import Depends

from api.v1.models.file import UploadFileResponse, UploadFileStatusResponse
from core.jwt.token import BearerForm
from core.services import file_service as service

router = APIRouter()
logger = logging.getLogger('file_api')


@router.post('/file', response_model=UploadFileResponse)
def upload_file(
        data: bytes = File(...),
        _=Depends(BearerForm())
) -> UploadFileResponse:
    """Upload file.

    - input:
        - data: file
    - output:
        - UploadFileResponse: response with file hash and exired time
    """
    file_hash, exp = service.upload_file(data=data)
    return UploadFileResponse(
        file_hash=file_hash,
        exp=exp
    )


@router.get('/file', response_model=UploadFileStatusResponse)
def get_file_status(
        file_hash: str = Query(..., max_length=40),
        _=Depends(BearerForm())
) -> UploadFileStatusResponse:
    """
    Get file status.

    - input:
        - file_hash: file hash
    - output:
        - UploadFileStatusResponse: response with file status
    """
    file_status = service.get_file_status(file_hash=file_hash)
    return UploadFileStatusResponse(
        status=file_status
    )
