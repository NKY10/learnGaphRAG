import os
from core.llm import get_embedding
from typing import List, Optional
from langchain.schema import Document
from langchain_chroma import Chroma
class vectorDB:
    """向量存储类"""
    def __init__(self,cfg,ebd_cfg):
        """初始化向量存储"""
        self.persist_directory = cfg.chroma_path
        self.embeddings = get_embedding(ebd_cfg)
        self.vectorstore = None
        if self._connect_db():
            print(f"已连接到向量数据库{self.persist_directory}")
        else:
            print(f"向量数据库{self.persist_directory}不存在,使用create方法创建")
    def _check_available(self):
        """检查向量数据库是否可用"""
        if self.vectorstore is None:
            print(f"向量数据库{self.persist_directory}不存在")
            return False
        return True

    def _connect_db(self):
        """连接向量数据库"""
        if os.path.exists(self.persist_directory):
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
            return True
        return False

    def create(self,documents: List[Document]):
        """创建向量数据库"""
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        print(f"已创建向量数据库{self.persist_directory}")  

    def add_documents(self, documents: List[Document]):
        """添加文档到向量数据库"""
        if not self._check_available():
            raise FileNotFoundError(f"向量数据库{self.persist_directory}不存在")
        self.vectorstore.add_documents(documents)
        print(f"已添加文档到向量数据库{self.persist_directory}")

    def search(self, query: str, k: int = 5):
        """搜索向量数据库"""
        if not self._check_available():
            raise FileNotFoundError(f"向量数据库{self.persist_directory}不存在")
        return self.vectorstore.similarity_search(query, k=k)
    
    def delete(self):
        """删除向量数据库"""
        if not self._check_available():
            raise FileNotFoundError(f"向量数据库{self.persist_directory}不存在")
        self.vectorstore.delete_collection()
        self.vectorstore = None
        print(f"已删除向量数据库{self.persist_directory}")
