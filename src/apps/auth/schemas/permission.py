from pydantic import BaseModel, Field
from typing import Optional, List
from src.enums.base import Action

class Permission(BaseModel):
    module: Optional[str] = Field(None, max_length=100)
    action: Optional[Action] = Action.CREATE


class PermissionGroup(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    permission_ids: Optional[List[str]] = []
