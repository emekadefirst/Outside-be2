from fastapi import BackgroundTasks
from tortoise.expressions import Q
from src.utilities.base_service import BOA
from src.models.user_models import User
from src.utilities.errorHandler import ErrorMessage
from src.schemas.user_schema import RegisterDto, LoginDto, Profile
from src.utilities.hash import verify_password
from src.utilities.crypto_func import JWTService


class AuthService:
    boa = BOA(User)
    error = ErrorMessage(User)
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

        user = await cls.boa.create(**dto.dict())
        # Optional background task
        # task.add_task(send_welcome_email, user.email)

        return cls.jwt.generate_token({"user_id": str(user.id)})

    @classmethod
    async def login(cls, dto: LoginDto):
        user = await cls.boa.get_or_404(email=dto.email)

        hsh = verify_password(user.password, dto.password)
        if not hsh:
            raise cls.error.unauthorized()

        return cls.jwt.generate_token({"user_id": str(user.id)})

    @classmethod
    async def stats(cls):
        return await cls.boa.model.all().count()
    
    @classmethod
    async def list(cls):
        return await cls.boa.all()


        

