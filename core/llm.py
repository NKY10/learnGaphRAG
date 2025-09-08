from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_ollama import ChatOllama, OllamaEmbeddings
from core.config import LLMConfig, EmbeddingConfig

def get_llm(config:LLMConfig):
    if config.type == "openai":
        return ChatOpenAI(
            openai_api_key=config.api_key,
            openai_api_base=config.api_base,
            model_name=config.model,
            temperature=0,
        )
    elif config.type == "ollama":
        return ChatOllama(
            model=config.model,
            temperature=0,
        )
    else:
        raise ValueError(f"不支持的LLM类型: {config.type}")

def get_embedding(config:EmbeddingConfig):
    if config.type == "openai":
        return OpenAIEmbeddings(
            openai_api_key=config.api_key,
            openai_base_url=config.api_base,
            model_name=config.model,
        )
    elif config.type == "ollama":
        return OllamaEmbeddings(
            model=config.model,
        )
    else:
        raise ValueError(f"不支持的Embedding类型: {config.type}")