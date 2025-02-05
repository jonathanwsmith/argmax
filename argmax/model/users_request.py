from typing import Optional

from pydantic import BaseModel


class UsersRequest(BaseModel):
    query: Optional[str] = None
