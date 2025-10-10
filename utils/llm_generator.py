from openai import AzureOpenAI
from dotenv import load_dotenv
import os

#constants
load_dotenv()
LLM_MODEL_AZURE = "gpt-35-turbo"
EMBEDDING_MODEL_AZURE = "text-embedding-3-large"
API_KEY_AZURE = os.getenv('API_KEY_AZURE')
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")
ENDPOINT_AZURE = os.getenv("ENDPOINT_AZURE")

def init_azure_client() -> AzureOpenAI:
    return AzureOpenAI(
            azure_endpoint=ENDPOINT_AZURE,
            api_key=API_KEY_AZURE,
            api_version=AZURE_API_VERSION
    )

def embed_query(client_azure: AzureOpenAI, query: list) -> list[float]:
    return client_azure.embeddings.create(
        input=query,
        model=EMBEDDING_MODEL_AZURE
    ).data[0].embedding

def response_generator(client_azure: AzureOpenAI, system_prompt: str, user_prompt: str) -> str:
    response = client_azure.chat.completions.create(
        model="gpt-35-turbo",
        messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
    )

    return response.choices[0].message.content