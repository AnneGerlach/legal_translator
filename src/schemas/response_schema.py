from pydantic import BaseModel, Field


class StandardResponseSchema(BaseModel):
    result: str = Field(
        ...,
        description="output text",
        examples=["output_text"]
    )


standard_response_examples = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "first_standard_response": {
                        "value": {
                            "text": "output1"
                        }
                    },
                    "second_standard_response": {
                        "value": {
                            "text": "output2"
                        }
                    }
                }
            }
        }
    }
}