# RemakeGraphrag 开发指南

## 项目概述

RemakeGraphrag 是一个基于 Python 的 GraphRAG 实现项目，旨在复现 nano-graphrag 的核心功能。该项目使用了现代化的技术栈，包括 Neo4j 图数据库、ChromaDB 向量数据库，以及 LangChain 框架。

## 当前项目状态

### 已完成功能
- ✅ 环境配置和依赖管理
- ✅ 图数据库连接和基础操作 (Neo4j)
- ✅ 实体和关系的数据模型定义
- ✅ LLM 实体关系提取功能
- ✅ 基础的图数据存储和查询

### 待实现功能
- 🔄 文本分块处理
- 🔄 向量嵌入和相似性搜索
- 🔄 图聚类算法 (Leiden 算法)
- 🔄 社区报告生成
- 🔄 Local 和 Global 查询模式
- 🔄 增量更新支持

## 核心架构设计

### 推荐的类设计

#### 1. GraphRAGManager (`utils/worker.py`)
负责所有数据库操作和数据处理流程：

```python
class GraphRAGManager:
    """GraphRAG 数据库操作管理类"""
    
    def __init__(self, mcfg: LLMConfig, ecfg: EmbeddingConfig, 
                 gcfg: GraphConfig, vcfg: ChromaConfig):
        self.llm = get_llm(mcfg)
        self.gdb = graphDB(gcfg)
        self.vdb = vectorDB(vcfg, ecfg)
        self.embedding_func = get_embedding(ecfg)
        self.structure_llm = self.llm.with_structured_output(LLMOutput)
    
    # 核心功能方法
    def chunk_text(self, text: str) -> List[Dict]:
        """基于token大小的文本分块"""
        
    def extract_entities(self, chunks: List[str]) -> LLMOutput:
        """LLM实体和关系提取"""
        
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
```

#### 2. GraphRAG (`rag.py`)
提供查询接口的最终用户类：

```python
class GraphRAG:
    """GraphRAG 查询类 - 用户接口"""
    
    def __init__(self, llm_config: LLMConfig, embedding_config: EmbeddingConfig,
                 graph_config: GraphConfig, vector_config: ChromaConfig):
        self.manager = GraphRAGManager(llm_config, embedding_config, 
                                       graph_config, vector_config)
        
    def insert(self, text: str):
        """插入文档并处理"""
        return self.manager.process_document(text)
        
    def query(self, question: str, mode: str = "local") -> str:
        """查询接口
        
        Args:
            question: 用户问题
            mode: 查询模式 ("local", "global", "naive")
            
        Returns:
            str: 回答结果
        """
        if mode == "local":
            return self._local_query(question)
        elif mode == "global":
            return self._global_query(question)
        elif mode == "naive":
            return self._naive_query(question)
        else:
            raise ValueError(f"Unknown mode: {mode}")
    
    def _local_query(self, question: str) -> str:
        """本地查询 - 基于实体相似性"""
        
    def _global_query(self, question: str) -> str:
        """全局查询 - 基于社区报告"""
        
    def _naive_query(self, question: str) -> str:
        """朴素查询 - 传统向量检索"""
```

### 项目结构

```
remakeGraphrag/
├── core/                    # 配置和数据模型
│   ├── config.py           # 配置类
│   ├── schema.py           # 数据模型
│   └── llm.py              # LLM工具
├── utils/                   # 工具模块
│   ├── graphDB.py          # Neo4j操作
│   ├── vectorDB.py         # ChromaDB操作
│   ├── worker.py           # GraphRAGManager
│   └── prompts.py          # 提示词
├── rag.py                   # GraphRAG主类
├── test/                    # 测试文件
├── examples/                # 使用示例
└── requirements.txt         # 依赖
```

### 使用示例

```python
# 基本使用
from rag import GraphRAG
from core.config import LLMConfig, EmbeddingConfig, GraphConfig, ChromaConfig

# 初始化
rag = GraphRAG(
    llm_config=LLMConfig(),
    embedding_config=EmbeddingConfig(),
    graph_config=GraphConfig(), 
    vector_config=ChromaConfig()
)

# 处理文档
rag.insert("""
这里放入你的文档内容...
""")

# 查询
result = rag.query("什么是GraphRAG？", mode="local")
print(result)

# 不同模式查询
local_result = rag.query("文档中提到了哪些关键概念？", mode="local")
global_result = rag.query("这篇文档的主要主题是什么？", mode="global")
naive_result = rag.query("文档中关于X的信息", mode="naive")
```

## 详细实现计划

### 阶段一：完善核心类 (Week 1-2)

#### 1.1 增强 GraphRAGManager 类 (`utils/worker.py`)
基于现有的 `BuildGrpah` 类扩展功能：

```python
# 重命名 BuildGrpah 为 GraphRAGManager
class GraphRAGManager:
    def __init__(self, mcfg: LLMConfig, ecfg: EmbeddingConfig, 
                 gcfg: GraphConfig, vcfg: ChromaConfig):
        # 现有初始化代码
        self.llm = get_llm(mcfg)
        self.gdb = graphDB(gcfg)
        self.vdb = vectorDB(vcfg, ecfg)
        self.extract_prompt = extract_prompt
        self.structure_llm = self.llm.with_structured_output(LLMOutput)
        
        # 新增功能
        self.embedding_func = get_embedding(ecfg)
        
    def chunk_text(self, text: str, chunk_size: int = 1200, overlap: int = 100) -> List[Dict]:
        """基于token大小的文本分块"""
        # 实现文本分块逻辑
        
    def extract_entities(self, chunks: List[str]) -> LLMOutput:
        """批量提取实体和关系"""
        # 基于现有 extract_entities 方法扩展
        
    def process_document(self, text: str) -> bool:
        """完整的文档处理流程"""
        # 1. 文本分块
        # 2. 实体提取
        # 3. 构建图谱
        # 4. 向量化
        # 5. 图聚类
        # 6. 生成报告
        
    def embed_entities(self, entities: List[Entity]):
        """实体向量化"""
        # 实体名称和描述的向量化
        
    def cluster_communities(self, algorithm: str = "leiden"):
        """图聚类算法"""
        # 实现Leiden算法
        
    def generate_community_reports(self):
        """生成社区报告"""
        # 基于聚类结果生成报告
```

#### 1.2 创建 GraphRAG 主类 (`rag.py`)
```python
class GraphRAG:
    def __init__(self, llm_config: LLMConfig, embedding_config: EmbeddingConfig,
                 graph_config: GraphConfig, vector_config: ChromaConfig):
        self.manager = GraphRAGManager(llm_config, embedding_config, 
                                       graph_config, vector_config)
        
    def insert(self, text: str) -> bool:
        """插入文档并处理"""
        return self.manager.process_document(text)
        
    def query(self, question: str, mode: str = "local") -> str:
        """查询接口"""
        if mode == "local":
            return self._local_query(question)
        elif mode == "global":
            return self._global_query(question)
        elif mode == "naive":
            return self._naive_query(question)
        else:
            raise ValueError(f"Unknown mode: {mode}")
            
    def _local_query(self, question: str) -> str:
        """本地查询 - 基于实体相似性"""
        # 1. 向量化问题
        # 2. 检索相关实体
        # 3. 构建子图
        # 4. 生成回答
        
    def _global_query(self, question: str) -> str:
        """全局查询 - 基于社区报告"""
        # 1. 分析问题
        # 2. 选择相关社区
        # 3. 整合社区报告
        # 4. 生成回答
        
    def _naive_query(self, question: str) -> str:
        """朴素查询 - 传统向量检索"""
        # 1. 向量化问题
        # 2. 检索相关文本块
        # 3. 生成回答
```

#### 1.3 更新依赖和配置
- 更新 `requirements.txt` 添加必要依赖
- 完善 `core/config.py` 配置类
- 添加文本分块和聚类算法的配置

### 阶段二：核心功能实现 (Week 3-4)

#### 2.1 文本处理管道
- 实现基于 token 大小的文本分块
- 支持自定义分块策略
- 实现文本块的去重和增量更新

#### 2.2 实体提取增强
- 集成 DSPY 实体提取（可选）
- 实现实体消歧和融合
- 支持实体关系强度计算

#### 2.3 向量化处理
- 实现实体名称和描述的向量化
- 支持多种嵌入模型（OpenAI、本地模型）
- 实现向量相似性搜索

#### 2.4 图聚类算法
- 实现 Leiden 聚类算法
- 支持社区检测和层次化聚类
- 生成社区报告

### 阶段三：查询引擎 (Week 5-6)

#### 3.1 Local 查询模式
- 基于实体相似性的本地搜索
- 结合向量检索和图遍历
- 生成上下文相关的回答

#### 3.2 Global 查询模式
- 基于社区报告的全局搜索
- 实现多跳推理
- 支持复杂问题分解

#### 3.3 Naive RAG 模式
- 实现传统的向量检索
- 作为基准对比模式

### 阶段四：高级功能 (Week 7-8)

#### 4.1 增量更新
- 支持新文档的增量处理
- 避免重复计算
- 保持图的一致性

#### 4.2 性能优化
- 实现异步处理
- 批量操作优化
- 缓存机制

#### 4.3 监控和调试
- 实现处理进度跟踪
- 添加日志和监控
- 性能基准测试

## 技术选型建议

### 存储层
- **图数据库**: 保持 Neo4j（已实现），可选 NetworkX（轻量级）
- **向量数据库**: 保持 ChromaDB，可选 FAISS、Milvus
- **键值存储**: JSON 文件（简单），可选 Redis（生产环境）

### 处理层
- **文本分块**: TikToken（推荐），HuggingFace Tokenizer
- **实体提取**: LangChain + LLM，可选 DSPY
- **图聚类**: Leiden 算法（igraph），可选 Louvain
- **嵌入模型**: OpenAI text-embedding-3-small，可选本地模型

### 查询层
- **LLM**: GPT-4o（高质量），GPT-4o-mini（经济）
- **缓存**: 内存缓存 + 持久化缓存
- **异步处理**: asyncio + aiohttp

## 开发建议

### 代码质量
1. **类型注解**: 全面使用 Python 类型注解
2. **单元测试**: 保持高测试覆盖率
3. **文档**: 添加详细的 docstring
4. **错误处理**: 实现优雅的错误处理机制

### 性能考虑
1. **批量操作**: 尽量使用批量数据库操作
2. **异步处理**: 大量 I/O 操作使用异步
3. **内存管理**: 注意大数据集的内存使用
4. **缓存策略**: 合理使用缓存提高性能

### 扩展性设计
1. **插件化**: 支持自定义组件替换
2. **配置驱动**: 通过配置文件控制行为
3. **接口抽象**: 清晰的接口定义便于扩展
4. **模块化**: 松耦合的模块设计

## 实现优先级

### P0 (核心功能)
- [ ] 完整的文本处理管道
- [ ] 实体提取和关系构建
- [ ] 图聚类和社区报告
- [ ] Local 和 Global 查询

### P1 (重要功能)
- [ ] 向量化处理和相似性搜索
- [ ] 增量更新支持
- [ ] 性能优化
- [ ] 完整的测试套件

### P2 (增强功能)
- [ ] 多种存储后端支持
- [ ] 高级配置选项
- [ ] 监控和调试工具
- [ ] 示例和文档完善

## 下一步行动

1. **立即开始**: 重构项目结构，实现基础接口
2. **第一周**: 完成文本处理和实体提取
3. **第二周**: 实现图聚类和社区报告
4. **第三周**: 开发查询引擎
5. **第四周**: 性能优化和测试

## 相关资源

- [nano-graphrag 源码](../nano-graphrag/)
- [GraphRAG 论文](https://arxiv.org/pdf/2404.16130)
- [Neo4j 文档](https://neo4j.com/docs/)
- [ChromaDB 文档](https://docs.trychroma.com/)
- [LangChain 文档](https://python.langchain.com/)

---

*本指南将根据项目进展持续更新，建议定期查看最新版本。*