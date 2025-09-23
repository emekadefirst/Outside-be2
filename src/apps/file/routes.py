from src.utilities.route_builder import build_router
from src.apps.file.services import FileService, List, UploadFile, Optional

file_router = build_router(path="files", tags=["Files"])

@file_router.post("/", status_code=201)
async def upload(files: Optional[List[UploadFile]] = None):
    return await FileService.upload(files)