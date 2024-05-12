from src.schema.base import BaseModelSchema


class UserSchema(BaseModelSchema):
    username: str
    is_admin: bool
