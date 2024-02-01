import uuid
from typing import Any, Mapping, TypeVar

from pydantic import BaseModel, ConfigDict, Field, GetCoreSchemaHandler
from pydantic_core import core_schema
from pydantic_core.core_schema import CoreSchema, ValidationInfo
from pymongo.collection import Collection

class StrUUID(str):
    """
    UUID validation but keeping it as a string.
    """

    def __new__(cls, string=None):
        if string is None:
            string = str(uuid.uuid4())
        return super().__new__(cls, string)

    @classmethod
    def __get_pydantic_core_schema__(
            cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(str))

    @classmethod
    def validate(cls, v, info: ValidationInfo):
        if isinstance(v, uuid.UUID):
            # If UUID is given, format is already verified, we just need to cast to string
            return cls(str(v))
        if not isinstance(v, str):
            raise TypeError("string required")
        uuid.UUID(v)
        # raises ValueError if it doesn't work. We don't need to
        # actually keep the uuid object, just check its format

        return cls(v)

    def __repr__(self):
        return f"StrUUID({super().__repr__()})"


class Document(BaseModel):
    id: StrUUID = Field(default_factory=StrUUID)
    schema_version: str = "0.0.1"

    model_config = ConfigDict(extra="forbid")

    class Settings:
        collection_name: str = ""

    def __init__(self, **kwargs):
        if kwargs.get("_id"):
            kwargs["id"] = kwargs.pop("_id")
        super().__init__(**kwargs)

    @classmethod
    def _get_collection_name(cls, ) -> str:
        return cls.Settings.collection_name

    @classmethod
    def _get_collection_from_name(cls, name: str) -> Collection:
        return get_db()[name]

    @classmethod
    def collection(cls, ) -> Collection:
        name = cls._get_collection_name()
        if not name:
            raise ValueError(f"{cls}.Settings.collection_name is missing!")
        return cls._get_collection_from_name(name)

    def save(self):
        """Inserts or updates a document with this id in the database"""
        self.collection().replace_one(
            {"_id": self.id},
            self.model_dump(exclude={"id"}),
            upsert=True,
        )
        return self

    @classmethod
    def get(cls, id: StrUUID, *args, **kwargs):
        """
        Shortcut method that retrieves a document and instantiates the python object (model) for it
        """
        doc = cls.collection().find_one(id, *args, **kwargs)
        if doc is not None:
            doc = cls(**doc)
        return doc

    @classmethod
    def find(cls, filter: Mapping[str, Any] | None = None, *args, **kwargs):
        """
        Shortcut method that retrieves all document and instantiates the models for them.
        """
        if filter is None:
            filter = {}
        return [cls(**doc) for doc in cls.collection().find(filter, *args, **kwargs)]




