from tortoise import fields
from src.utilities.base_model import BaseModel


class Event(BaseModel):
    host = fields.ForeignKeyField("models.User", related_name="event_host", on_delete=fields.CASCADE)
    title = fields.CharField(max_length=155, unique=True)
    description = fields.TextField(null=True)
    time = fields.JSONField()  
    banner = fields.ForeignKeyField("models.File", related_name="event_banner", null=True, on_delete=fields.SET_NULL)
    gallery = fields.ManyToManyField("models.File", related_name="event_gallery")
    latitude = fields.FloatField(null=True)
    longitude = fields.FloatField(null=True)
    address = fields.CharField(max_length=500)

    def __str__(self):
        return self.title

    class Meta:
        table = "events"
        ordering = ["-created_at"]


