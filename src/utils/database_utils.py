
from src.config.database import db, env
from src.models.models import StandardModel


def add_document_to_collection(document: StandardModel):
    # insert_obj
    db.get_collection(env.db_collection).insert_one(
        document.dict()
    )


def find_document_in_collection():
    db_documents = list(db.get_collection(env.db_collection).find({"user_id": "Anne"}))
    print(db_documents)  # noqa: T201