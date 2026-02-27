self.qdrant_client = QdrantClient(
    host=settings.qdrant_host,
    port=settings.qdrant_port,
)

self.vectorstore = QdrantVectorStore(
    client=self.qdrant_client,
    collection_name="destinations",
    embedding=embeddings,
    content_payload_key="description",
)
