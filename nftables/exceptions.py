from pydantic import BaseModel

class HTTP_OK(BaseModel):
    data  : dict
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "HTTP Method OK"},
        }


class HTTPError(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "nftables error raised."},
        }

