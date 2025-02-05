from typing import List

from pydantic import BaseModel

from argmax.model import DetectionResult


class UsersResponse(BaseModel):
    items: List[DetectionResult]
