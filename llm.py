import os
from abc import ABC, abstractmethod
from google import genai


class LLM(ABC):
    @abstractmethod
    async def generate(self):
        pass

class GeminiLLM(LLM):
    def __init__(self, question):
        self.__client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.__question = question

    async def generate(self):
        response = self.__client.models.generate_content(
            model="gemini-2.0-flash", contents=self.__question
        )

        return response.text
