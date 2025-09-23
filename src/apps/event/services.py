from src.utilities.base_service import BaseModelService
from src.error.base import ErrorHandler
from src.apps.event import Event
from src.apps.file import File
from src.apps.auth import User
from src.apps.event.schemas import EventSchema

class EventService:
    boa = BaseModelService(Event, methods=[lambda q: q.prefetch_related("banner", "gallery")])
    model = Event
    error = ErrorHandler
    file = BaseModelService(File)
    user = BaseModelService(User)

    @classmethod
    async def list(cls):
        return await cls.boa.list_active()
    

    @classmethod
    async def create(cls, dto: EventSchema) -> Event:
        host = await cls.user.get_object_or_404(id=dto.host_id)
        banner = await cls.file.get_object_or_404(id=dto.banner_id)
        data = dto.dict(exclude_unset=True, exclude={"host_id", "banner_id", "gallery"})
        event = await cls.model.create(**data, host=host, banner=banner)
        if dto.gallery:
            files = []
            for content in dto.gallery:
                f = await cls.file.get_object_or_404(id=content)
                files.append(f)
            await event.gallery.add(*files)
        return event

    @classmethod
    async def update(cls, id: str, dto: EventSchema) -> Event:
        obj = await cls.boa.get_object_or_404(id=id)
        for field, value in dto.dict(exclude_unset=True).items():
            setattr(obj, field, value)
        await obj.save()
        return obj
    
    @classmethod
    async def list(cls):
        return await cls.boa.list_active()
