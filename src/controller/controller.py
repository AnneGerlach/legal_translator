from pydantic import BaseModel

from src.models.models import LegalTranslation
from src.utils.database_utils import add_document_to_collection
from src.utils.request_utils import request_chat_completion


class StandardController(BaseModel):
    standard_model: LegalTranslation

    async def initialize_standard_controller(self):

        self.standard_model.prompt = [{"role": "assistant",
                                       "content": f"Let's work this out in a step by step way, "
                                                  f"to be sure we have the right answer. "
                                                  f"Formuliere diesen Text in leichter Sprache und "
                                                  f"fasse ihn in Stichpunkten zusammen: "
                                                  f"{self.standard_model.text}"}]

        self.standard_model.result = request_chat_completion(self.standard_model.text, self.standard_model.prompt)

        add_document_to_collection(self.standard_model)
