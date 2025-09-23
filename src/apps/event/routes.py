from src.apps.auth.models.user import User
from src.apps.event import Event
from fastapi import BackgroundTasks, Depends
from src.utilities.route_builder import build_router
from src.enums.base import Action, AppModule
from src.utilities.crypto_func import JWTService
from src.apps.event.schemas import EventSchema
from src.apps.event.services import EventService
from src.dependencies.permission import AuthPermissionService


user = JWTService()
event_router = build_router(path="events", tags=["Event"])



@event_router.get("/", status_code=200)
async def get_all():
    return await EventService.list()
