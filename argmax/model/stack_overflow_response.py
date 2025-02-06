import datetime
from typing import List, Optional

from pydantic import BaseModel, AnyHttpUrl, HttpUrl


class BadgeCounts(BaseModel):
    bronze: int
    silver: int
    gold: int


class SOUser(BaseModel):
    about_me: Optional[str] = None
    accept_rate: Optional[int] = None
    account_id: int
    age: Optional[int] = None
    answer_count: Optional[int] = None
    badge_counts: BadgeCounts
    creation_date: datetime.datetime
    display_name: str
    down_vote_count: Optional[int] = None
    is_employee: bool
    last_modified_date: datetime.datetime
    last_access_date: datetime.datetime
    link: HttpUrl
    location: Optional[str] = None
    profile_image: HttpUrl
    question_count: Optional[int] = None
    reputation: int
    reputation_change_day: int
    reputation_change_month: int
    reputation_change_quarter: int
    reputation_change_week: int
    reputation_change_year: int
    timed_penalty_date: Optional[datetime.datetime] = None
    user_id: int
    user_type: str
    view_count: Optional[int] = None
    website_url: HttpUrl


class StackOverflowResponse(BaseModel):
    backoff: Optional[int] = None
    error_id: Optional[int] = None
    error_message: Optional[str] = None
    error_name: Optional[str] = None
    has_more: bool
    items: List[SOUser]
    page: Optional[int] = None
    page_size: Optional[int] = None
    quota_max: int
    quota_remaining: int
    total: Optional[int] = None
    type: Optional[str] = None
