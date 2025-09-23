from src.utilities.base_model import BaseModel
from src.enums.base import PaymentGateway, PaymentStatus, PaymentType
from tortoise import fields
from tortoise.exceptions import ValidationError
from datetime import datetime

class Payout(BaseModel):
    host = fields.ForeignKeyField("models.User", related_name="payouts", on_delete=fields.CASCADE)
    event = fields.ForeignKeyField("models.Event", related_name="payouts", on_delete=fields.CASCADE)
    total = fields.DecimalField(max_digits=12, decimal_places=2)
    paid_at = fields.DatetimeField(null=True)
    status = fields.CharEnumField(PaymentStatus, default=PaymentStatus.PENDING)
    payment_ref_id = fields.CharField(255, null=True, unique=True)

    def __str__(self):
        return f"Payout for {self.event.name} to {self.host.username} - {self.total}"

    class Meta:
        table = "payouts"
        ordering = ["-created_at"]
