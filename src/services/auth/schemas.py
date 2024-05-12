from pydantic import BaseModel


class PayloadSchema(BaseModel):
    username: str
    password: str


class AccessTokenSchema(BaseModel):
    access_token: str
