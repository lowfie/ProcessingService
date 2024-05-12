from pydantic import BaseModel, ConfigDict, Field

from src.schema.receiver import ReceiverSchema


class ReceiverRequestSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    timestamp: int
    a: int | None = Field(default=None, ge=1, alias="A")
    b: int | None = Field(default=None, ge=1, alias="B")
    c: int | None = Field(default=None, ge=1, alias="C")
    d: int | None = Field(default=None, ge=1, alias="D")
    e: int | None = Field(default=None, ge=1, alias="E")
    f: int | None = Field(default=None, ge=1, alias="F")


class ReceiversSchema(BaseModel):
    receivers: list[ReceiverSchema]
    total_pages: int
    total_items: int


class ReceiversUsersSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    user_id: int
    total_a: int | None
    total_b: int | None
    total_c: int | None
    total_d: int | None
    total_e: int | None
    total_f: int | None
