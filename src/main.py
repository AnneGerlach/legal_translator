import logging
from logging.config import dictConfig

import uvicorn
from fastapi import FastAPI
from google.cloud.logging_v2 import Client
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.middleware.cors import CORSMiddleware

from src.config.config import (
    APP_NAME,
    CONTACT_EMAIL,
    CONTACT_PERSON,
    DESCRIPTION,
    VERSION,
    LogConfig,
    get_settings,
)
from src.routes.routes import myresource_router

fastapi_app = FastAPI(title=APP_NAME,
              description=DESCRIPTION,
              version=VERSION,
              contact={
                  "name": CONTACT_PERSON,
                  "email": CONTACT_EMAIL,
              })

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db_client(settings):
    return AsyncIOMotorClient(settings.mdb_connection_string, tz_aware=True)


def include_routers(fastapi_app: FastAPI):
    print("include router") # noqa: T201
    fastapi_app.include_router(myresource_router)


@fastapi_app.on_event("startup")
async def app_init():
    """
    Setups logging, connects to database, initializes ODM and include routers in the app.
    """
    env = get_settings()
    if env.is_deployed_locally():
        # if True:
        # LOAD CONFIG LOCAL_CONFIG
        dictConfig(LogConfig().dict())
    else:
        #
        google_client = Client(project=get_settings().gcp_project_number)
        google_client.get_default_handler()
        google_client.setup_logging()

    include_routers(fastapi_app)
    logging.info(f"{APP_NAME}: Finished initializing")
    print("finish initialization") # noqa: T201


app = fastapi_app


if __name__ == "__main__":  # for debugging locally
    uvicorn.run("src.main:app",
                host="127.0.0.1",
                port=8080,
                
    )
    # sudo systemctl start mongod
    # run with `python -m src.main`
