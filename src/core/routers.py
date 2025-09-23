from src.apps.auth.routes.user import user_router
from src.apps.file.routes import file_router

routes = [
    user_router,
    file_router
]