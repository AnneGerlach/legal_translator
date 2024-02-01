from pymongo import MongoClient

from src.config.config import get_settings

env = get_settings()
DB_CLIENT = MongoClient(env.mdb_connection_string(),
                        uuidRepresentation="standard")
db = DB_CLIENT[env.db_name]


def get_db():
    return db[get_settings().db_name]