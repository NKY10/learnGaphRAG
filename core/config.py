# 读取.env

import os
from dotenv import load_dotenv
load_dotenv()

class LLMConfig:
    type = os.getenv("LLM_TYPE", "openai")
    model = os.getenv("MODEL")
    api_key = os.getenv("OPENAI_API_KEY")
    api_base = os.getenv("OPENAI_API_BASE")
    ollama_api = os.getenv("OLLAMA_API")

class EmbeddingConfig:
    type = os.getenv("EMBEDDING_TYPE", "ollama")
    model = os.getenv("EMBEDDING_MODEL")
    api_key = os.getenv("EMBEDDING_OPENAI_API_KEY")
    api_base = os.getenv("EMBEDDING_OPENAI_API_BASE")
    ollama_api = os.getenv("EMBEDDING_OLLAMA_API", os.getenv("OLLAMA_API"))

class GraphConfig:
    neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    neo4j_user = os.getenv("NEO4J_USER", "neo4j")
    neo4j_password = os.getenv("NEO4J_PASSWORD")

class ChromaConfig:
    chroma_path = os.getenv("CHROMA_PATH", "./chroma")
    collection_name = os.getenv("COLLECTION_NAME", "test")
