import openai
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class OpenAIEmbeddings:
    def __init__(self, model_name="text-embedding-3-small", api_key=None):
        self.model_name = model_name
        self.client = OpenAI(api_key=api_key)

    def embed_query(self, text):
        response = self.client.embeddings.create(
            input = [text],  # must be a list
            model = self.model_name
        )
        return response.data[0].embedding
