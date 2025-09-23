from src.utilities.base_model import BaseModel
from tortoise import fields
from src.utilities.hash import set_password

class User(BaseModel):
    first_name = fields.CharField(55, null=True)
    last_name = fields.CharField(55, null=True)
    email = fields.CharField(255, unique=True)
    phone_number = fields.CharField(20, unique=True)
    is_superuser = fields.BooleanField(default=False)
    is_staff = fields.BooleanField(default=False)
    is_host = fields.BooleanField(default=False)
    is_verified = fields.BooleanField(default=False)
    password = fields.CharField(128, null=True)
    permission_groups = fields.ManyToManyField("models.PermissionGroup", related_name="users")


    async def save(self, *args, **kwargs):
        if self.password: 
            self.password = set_password(self.password)
        await super().save(*args, **kwargs)

    class Meta:
        ordering = ["created_at", "updated_at"]
        table = "users"

    def __str__(self):
        return self.first_name