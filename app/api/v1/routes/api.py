from fastapi import APIRouter

from api.v1.routes import engine, face, file, ping, task, token, user

router = APIRouter()
router.include_router(ping.router, tags=['ping'])
router.include_router(token.router, tags=['token'])
router.include_router(user.router, tags=['user'])
router.include_router(engine.router, tags=['engine'])
router.include_router(file.router, tags=['file'])
router.include_router(task.router, tags=['task'])
router.include_router(face.router, tags=['face'])
