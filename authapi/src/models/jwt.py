from pydantic import BaseModel


class JWTToken(BaseModel):
    access_token: str
    refresh_token: str
