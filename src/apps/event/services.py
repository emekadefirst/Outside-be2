from src.utilities.base_service import BaseModelService
from src.error.base import ErrorHandler
from src.apps.event import Event
from src.apps.file import File
from src.apps.auth import User
from src.apps.event.schemas import EventSchema
from typing import List, Dict

class EventService:
    boa = BaseModelService(Event)
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
    async def list(cls) -> List[Dict]:
        events = (
            await cls.model.all()
            .select_related("host", "banner")
            .prefetch_related("gallery")
        )

        results = []
        for e in events:
            results.append({
                "id": str(e.id),
                "title": e.title,
                "description": e.description,
                "time": e.time,
                "latitude": e.latitude,
                "longitude": e.longitude,
                "address": e.address,
                "host": {
                    "id": str(e.host.id),
                    "email": e.host.email,
                    "name": f"{e.host.first_name} {e.host.last_name}"
                } if e.host else None,
                "banner": e.banner.url if e.banner else None,
                "gallery": [f.url for f in e.gallery],
            })
        return results
