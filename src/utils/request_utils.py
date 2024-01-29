import openai

from src.config.database import env


def request_chat_completion(text: str, chat_message: list) -> str:

    openai.api_key = env.openai_api_key

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_message,
        temperature=0.2
    )

    return response["choices"][0]["message"]["content"]