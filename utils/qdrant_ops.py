from qdrant_client.models import Filter, FieldCondition, MatchText
from qdrant_client import QdrantClient
from .llm_generator import embed_query, init_azure_client
from dotenv import load_dotenv
import os

# constants
load_dotenv()
COLLECTION_NAME = "recipe_rag_collection"
URL_QDRANT = os.getenv("URL_QDRANT")
API_KEY_QDRANT = os.getenv("API_KEY_QDRANT")

def init_qdrant_client() -> QdrantClient:
    return QdrantClient(
            url=URL_QDRANT,
            api_key=API_KEY_QDRANT
    )

def retrieve_similar_recipes(client_qdrant: QdrantClient, query_emb: list, top_k: int = 10):
    results = client_qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=query_emb,
        limit=top_k
    )

    return results.points


def query_by_title(client_qdrant: QdrantClient, title: str) -> dict or None:
    query_vector = embed_query(init_azure_client(), title)

    results = retrieve_similar_recipes(
        client_qdrant=init_qdrant_client(),
        query_emb=query_vector,
        top_k=1
    )

    if results:
        return results[0].payload

    return None

