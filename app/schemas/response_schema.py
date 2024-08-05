# from pydantic import BaseModel
# from typing import Union, Optional


# class ResponseSchema(BaseModel):
#     status: bool = True
#     response: Optional[str]= None
#     data: Union[Optional[dict], Optional[list], None] = None

#     class Config():
#         # orm_mode = True
#         from_attributes=True





from pydantic import BaseModel
from typing import TypeVar, Generic, Optional, List

T = TypeVar('T')

class ResponseSchema(BaseModel, Generic[T]):
    status: bool
    response: str
    data: Optional[T] = None

    class Config:
        from_attributes = True
