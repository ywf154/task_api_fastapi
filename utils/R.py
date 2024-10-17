from typing import Optional, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar('T')


class R(BaseModel, Generic[T]):
    code: int
    msg: str
    data: Optional[T] = None

    @classmethod
    def success(cls, data: Optional[T] = None) -> 'R[T]':
        return cls(code=0, msg="操作成功", data=data)

    @classmethod
    def error(cls, msg: str) -> 'R':
        return cls(code=1, msg=msg, data=None)