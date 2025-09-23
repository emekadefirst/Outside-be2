from tortoise import fields
from tortoise.exceptions import ValidationError
from datetime import datetime

from src.utilities.base_model import BaseModel
from src.enums.base import PaymentGateway, PaymentStatus, PaymentType
from src.utilities.id_gen import generate_ticket_id



class Payin(BaseModel):
    provider = fields.CharEnumField(PaymentGateway)
    ticket = fields.ForeignKeyField("models.Ticket", related_name="payins", on_delete=fields.CASCADE)
    quantity = fields.IntField()
    total_cost = fields.DecimalField(max_digits=10, decimal_places=2)
    status = fields.CharEnumField(PaymentStatus, default=PaymentStatus.PENDING)
    payment_ref_id = fields.CharField(max_length=255, null=True, unique=True)

    user = fields.ForeignKeyField("models.User", related_name="payins", on_delete=fields.SET_NULL, null=True)
    email = fields.CharField(max_length=255, null=True)
    fullname = fields.CharField(max_length=255, null=True)
    phone_number = fields.CharField(max_length=20, null=True)

    payment_type = fields.CharEnumField(PaymentType, default=PaymentType.CASH)
    paid_at = fields.DatetimeField(null=True)

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError("Quantity must be positive")
        if self.quantity > self.ticket.quantity:
            raise ValidationError("Quantity exceeds available tickets")

    async def mark_success(self):
        """Mark payment as successful, deduct ticket stock, and issue orders."""
        self.status = PaymentStatus.SUCCESS
        self.paid_at = datetime.utcnow()
        await self.save()
        self.ticket.quantity -= self.quantity
        await self.ticket.save()
        for _ in range(self.quantity):
            serial = generate_ticket_id(self.ticket.event.title)
            await Order.create(ticket=self.ticket, serial_number=serial, payment=self)

    def __str__(self):
        return f"{self.quantity} x {self.ticket.name} for {self.ticket.event.title}"

    class Meta:
        table = "payins"
        ordering = ["-created_at"]


class Order(BaseModel):
    ticket = fields.ForeignKeyField("models.Ticket", related_name="orders", on_delete=fields.CASCADE)
    serial_number = fields.CharField(max_length=50, unique=True)
    issued_at = fields.DatetimeField(auto_now_add=True)
    delivery_mail = fields.JSONField(null=True)
    payment = fields.ForeignKeyField("models.Payin", related_name="orders", on_delete=fields.CASCADE)

    def __str__(self):
        return self.serial_number

    class Meta:
        table = "orders"
        ordering = ["created_at"]
