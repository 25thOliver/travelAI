from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from app.config import settings


class VectorService:
    def __init__(self):
        self.client = QdrantClient(
            host=settings.qdrant_host,
            port=settings.qdrant_port,
        )
        self.collection_name = "destinations"

    def create_collection(self):
        existing = [c.name for c in self.client.get_collections().collections]
        if self.collection_name not in existing:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=768,
                    distance=Distance.COSINE,
                ),
            )

    def upsert(self, id: int, vector: list[float], payload: dict):
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                {
                    "id": id,
                    "vector": vector,
                    "payload": payload,
                }
            ],
        )

    def search(self, vector: list[float], limit: int = 5):
        response = self.client.query_points(
            collection_name=self.collection_name,
            query=vector,
            limit=limit,
            query_filter={
                "must": [
                    {
                        "key": "country",
                        "match": {"value": "Kenya"}
                    }
                ]
            }
        )

        return response.points