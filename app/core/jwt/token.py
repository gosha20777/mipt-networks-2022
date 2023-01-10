from typing import Optional

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.requests import Request


class BearerForm(HTTPBearer):
    def __call__(
            self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        return
