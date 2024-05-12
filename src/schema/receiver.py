from src.schema.base import BaseModelSchema


class ReceiverSchema(BaseModelSchema):
    user_id: int
    timestamp: int
    a: int | None
    b: int | None
    c: int | None
    d: int | None
    e: int | None
    f: int | None
