from fastapi import BackgroundTasks
from tortoise.expressions import Q
from src.utilities.base_service import BaseModelService
from src.apps.auth.models.user import User
from src.error.base import ErrorHandler
from src.apps.auth.schemas.user import RegisterDto, LoginDto, Profile
from src.utilities.hash import verify_password
from src.utilities.crypto_func import JWTService


class AuthService:
    boa = BaseModelService(User)
    error = ErrorHandler(User)
    jwt = JWTService
    model = User()


    @classmethod
    async def stats(cls):
        return await cls.boa.model.count()


    @classmethod
    async def create(cls, dto: RegisterDto, task: BackgroundTasks):
        exists = await User.filter(Q(email=dto.email) | Q(phone_number=dto.phone_number)).first()
        if exists:
            raise cls.error.conflict("User with this email/username/phone already exists")

        user = await cls.model.create(**dto.dict())
        # Optional background task
        # task.add_task(send_welcome_email, user.email)
        return cls.jwt.generate_token(str(user.id))

    @classmethod
    async def login(cls, dto: LoginDto):
        user = await cls.boa.get_object_or_404(email=dto.email)
        hsh = verify_password(user.password, dto.password)
        if not hsh:
            raise cls.error.get(400)
        return cls.jwt.generate_token(str(user.id))

    @classmethod
    async def stats(cls):
        return await cls.boa.model.all().count()
    
    @classmethod
    async def list(cls):
        return await cls.boa.list_active()


        

