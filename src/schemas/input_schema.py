from pydantic import BaseModel, field_validator


class StandardInputSchema(BaseModel):
    input: str = "test"

    @field_validator("input")
    @classmethod
    def check_if_v_is_filled_string(cls, v):
        if not v:
            raise ValueError(f"Value {v} must be filled and not only an empty string")
        return v