from utils.prompts import extract_prompt
from utils.graphDB import graphDB
from utils.vectorDB import vectorDB
from core.config import GraphConfig,ChromaConfig,EmbeddingConfig,LLMConfig
from core.schema import LLMOutput,Entity,Relation
from core.llm import get_llm,get_embedding
from typing import List,Any,Dict
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
class GraphMaker:
    def __init__(
        self,
        mcfg:LLMConfig,
        ecfg:EmbeddingConfig,
        gcfg:GraphConfig,
        vcfg:ChromaConfig,
    ):
        self.llm = get_llm(mcfg)
        self.gdb = graphDB(gcfg)
        self.vdb = vectorDB(vcfg,ecfg)
        self.extract_prompt = extract_prompt
        self.structure_llm = self.llm.with_structured_output(LLMOutput)
    # 核心功能方法
    def chunk_text(self, text: str,size=1024,overlap=200) -> List[Document]:
        """基于token大小的文本分块"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=size,
            chunk_overlap=overlap,
            length_function=len,
        )
        return text_splitter.split_documents([Document(page_content=text)])
        
    def extract_entities(self, chunks: List[Document]) -> List[LLMOutput]:
        """LLM实体和关系提取"""
        results = []
        for chunk in chunks:
            prompt = self.extract_prompt.format(text=chunk.page_content)
            result = self.structure_llm.invoke(prompt)
            results.append(result)
        return results
        
    def build_graph(self, entities: List[Entity], relations: List[Relation]):
        """构建知识图谱到Neo4j"""
        
    def embed_entities(self, entities: List[Entity]):
        """实体向量化并存储到ChromaDB"""
        
    def process_document(self, text: str):
        """完整的文档处理流程"""
        
    def cluster_communities(self):
        """图聚类和社区检测"""
        
    def generate_community_reports(self):
        """生成社区报告"""