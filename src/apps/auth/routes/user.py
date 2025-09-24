from src.apps.auth.models.user import User
from fastapi import BackgroundTasks, Depends
from src.utilities.route_builder import build_router
from src.apps.auth.services.user import AuthService
from src.enums.base import Action, AppModule
from src.utilities.crypto_func import JWTService
from src.apps.auth.schemas.user import RegisterDto, LoginDto, UserResponseDto, Profile, RefreshToken
from src.dependencies.permission import AuthPermissionService


user = JWTService()
user_router = build_router(path="users", tags=["User"])


@user_router.get(
    "/",
    status_code=200, 
    response_model=list[UserResponseDto], 
    dependencies=[Depends(AuthPermissionService.permission_required(
        action=Action.READ,
        module=AppModule.USER
    ))]
)
async def all_users():
    return await AuthService.list()


@user_router.get("/whoami", status_code=200, response_model=UserResponseDto)
async def get_profile(current_user: User = Depends(user.get_current_user)):
    return current_user

@user_router.get(
    "/stats",
    status_code=200, 
    response_model=list[UserResponseDto], 
    dependencies=[Depends(AuthPermissionService.permission_required(
        action=Action.READ,
        module=AppModule.USER
    ))])
async def get_stats():
    return await AuthService.stats()

@user_router.post("/", status_code=201)
async def register_user(dto: RegisterDto, task: BackgroundTasks):
    return await AuthService.create(dto, task)

@user_router.post("/login", status_code=200)
async def login_user(dto: LoginDto):
    return await AuthService.login(dto)

@user_router.patch("/{user_id}", status_code=200, response_model=UserResponseDto)
async def update_user(user_id: str, dto: Profile):
    return await AuthService.models.update(id=user_id, dto=dto)


@user_router.post("/refresh", status_code=200)
async def refresh_token(dto: RefreshToken):
    return await user.refresh_token(refresh_token=dto.token)

@user_router.delete("/{user_id}", status_code=204)
async def update_user(user_id: str):
    return await AuthService.model.delete(id=user_id)