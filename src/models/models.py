import uuid

from pydantic import BaseModel, Field

from src.utils.utils import ts_now


class StandardModel(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    schema_version: str = "0.0.0"
    user_id: str
    text: str
    created_at: int | None = ts_now()
    result: str = None
    prompt: str = None


    class Config:
        json_encoders = {
            uuid.UUID: str,
        }