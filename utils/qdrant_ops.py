from qdrant_client.models import Filter, FieldCondition, MatchText
from qdrant_client import QdrantClient
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

def query_by_title(client_qdrant: QdrantClient, title: str) -> dict or None:
    search_filter = Filter(
        must=[
            FieldCondition(
                key="title",
                match=MatchText(text=title)
            )
        ]
    )

    search_result, _ = client_qdrant.scroll(
        collection_name=COLLECTION_NAME,
        scroll_filter=search_filter,
        limit=1,
        with_payload=True
    )

    if search_result:
        return search_result[0].payload


def retrieve_similar_recipes(client_qdrant: QdrantClient, query_emb: list, top_k: int = 10):
    results = client_qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=query_emb,
        limit=top_k
    )

    return results.points

