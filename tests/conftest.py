
from collections.abc import Callable
from functools import lru_cache

import pytest
from fastapi import FastAPI
from mongomock_motor import AsyncMongoMockClient

from src import main
from src.config import config
from src.config.config import Settings
from src.main import fastapi_app
from src.models.models import StandardModel

test_logs_file = "tests.log"


@lru_cache()
def get_test_settings():
    return config.Settings(mock_auth=True, deploy_environment=config.DeployEnvironments.TESTING)


@pytest.fixture(autouse=True, )
def override_settings(monkeypatch) -> None:
    monkeypatch.setattr(config, "get_settings", get_test_settings)


@pytest.fixture()
def test_settings() -> Settings:
    return get_test_settings()


@pytest.fixture(autouse=True)
async def db(monkeypatch):
    def mock_db_client(settings: Settings):
        return AsyncMongoMockClient(tz_aware=True)

    monkeypatch.setattr(main, "get_db_client", mock_db_client)



@pytest.fixture()
def app() -> FastAPI:
    fastapi_app.include_router("http://test", prefix="/tests")
    return fastapi_app


@pytest.fixture()
def standard_model_factory() -> Callable[..., StandardModel]:
    def _construct_example_model(
    ):
        return StandardModel(
            user_id="Anne",
            text="Test Text."
        )

    return _construct_example_model


