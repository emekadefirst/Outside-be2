from tortoise import fields
from src.utilities.base_model import BaseModel

class Ticket(BaseModel):
    event = fields.ForeignKeyField("models.Event", related_name="event_ticket", on_delete=fields.CASCADE)
    name = fields.CharField(max_length=55)
    cost = fields.DecimalField(max_digits=10, decimal_places=2)
    quantity = fields.IntField()

    def __str__(self):
        return f"{self.name} - {self.event.title}"

    class Meta:
        table = "tickets"
        ordering = ["created_at"]
