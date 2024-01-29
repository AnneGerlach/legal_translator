from pydantic import BaseModel, validator


class StandardInputSchema(BaseModel):
    input: str = "test"

    @validator("input")
    def check_if_v_is_filled_string(cls, v):     # noqa: N805
        if not v:
            raise ValueError(f"Value {v} must be filled and not only an empty string")
        return v