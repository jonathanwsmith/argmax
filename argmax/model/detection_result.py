from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

from argmax.model import BoundingBox


class DetectionResult(BaseModel):
    user_id: int
    display_name: str
    profile_image: str
    object_detected: bool
    bounding_boxes: Optional[List[BoundingBox]]
    detection_time_ms: float
