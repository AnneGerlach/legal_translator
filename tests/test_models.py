import pytest

from src.models.models import StandardModel


@pytest.mark.asyncio
async def test_standard_model(standard_model_factory):
    standard_model_obj = standard_model_factory()
    obj = StandardModel(**standard_model_obj.dict())
    assert obj.text
    assert obj.created_at
    assert obj.schema_version