import datetime

import pytz
from pydantic import Field

from src.documents import Document


class LegalTranslation(Document):
    user_id: str
    text: str
    created_at: str = Field(
        default_factory=lambda: datetime.datetime.now(tz=pytz.UTC).isoformat()
    )
    result: str | None = None
    prompt: str | None = None