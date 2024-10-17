from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class UserPydantic(BaseModel):
    id: int
    name: str
    password: Optional[str]

    class Config:
        from_attributes = True


class pydantic_create_plate(BaseModel):
    name: str
    uid: int


class PlatePydantic(BaseModel):
    id: int
    name: str
    uid: int


class pydantic_create_kind(BaseModel):
    name: str
    uid: int
    pid: int


class KindPydantic(BaseModel):
    id: int
    name: str
    uid: int
    pid: int


class TaskPydantic(BaseModel):
    id: Optional[int]
    name: str
    kid: int
    endTime: datetime
    status: Optional[bool]
    toWho: Optional[str] = None
    wxNoticeTo: Optional[str] = None
    wxNoticeFrom: Optional[str] = None
    createTime: Optional[datetime]
    finishTime: Optional[datetime] = None  # 设置为可选字段


class quick_create_task(BaseModel):
    name: str
    kid: int
    endTime: datetime


class info_user(BaseModel):
    pNames: List[str]
    kNames: List[str]
