from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field  


# 提取实体和关系的基础模型
class ExtractEntity(BaseModel):  
    entity_name: str = Field(description="实体的名称")  
    entity_type: str = Field(description="实体的类型")  
    entity_description: str = Field(description="实体的描述")  
  
class ExtractRelation(BaseModel):  
    source_entity: str = Field(description="关系的起始实体")  
    target_entity: str = Field(description="关系的目标实体")  
    relationship_description: str = Field(description="实体间关系的描述")  
    relationship_strength: int = Field(description="关系的强度,1-10之间的整数", ge=1, le=10)  

class LLMOutput(BaseModel):
    entities: List[ExtractEntity] = Field(description="提取的实体列表")
    relations: List[ExtractRelation] = Field(description="提取的关系列表")

# 图数据库中的实体模型
class Entity(ExtractEntity):  
    name_embedding: Optional[List[float]] = Field(  
        default=None,  
        description="实体名称的嵌入向量"  
    )  
    description_embedding: Optional[List[float]] = Field(  
        default=None,  
        description="实体描述的嵌入向量"  
    )  
    text_unit_ids: Optional[List[int]] = Field(  
        default=None,  
        description="包含该实体的文本单元ID列表"  
    ) 
  
class Relation(ExtractRelation):  
    description_embedding: Optional[List[float]] = Field(  
        default=None,  
        description="关系描述的嵌入向量"  
    )  
    text_unit_ids: Optional[List[int]] = Field(  
        default=None,  
        description="包含该关系的文本单元ID列表"  
    )  
    weight: Optional[float] = Field(  
        default=1.0,  
        description="关系权重"  
    )  
    rank: Optional[int] = Field(  
        default=1,  
        description="关系的重要性排名"  
    )

# ExtractEntity转换为Entity
def convert2entity(extract_entity: ExtractEntity, other: Dict[str, Any]) -> Entity:
    return Entity(
        entity_name=extract_entity.entity_name,
        entity_type=extract_entity.entity_type,
        entity_description=extract_entity.entity_description,
        text_unit_ids=other.get("text_unit_ids", None),
        name_embedding=other.get("name_embedding", None),
        description_embedding=other.get("description_embedding", None),
    )

# ExtractRelation转换为Relation
def convert2relation(extract_relation: ExtractRelation, other: Dict[str, Any]) -> Relation:
    return Relation(
        source_entity=extract_relation.source_entity,
        target_entity=extract_relation.target_entity,
        relationship_description=extract_relation.relationship_description,
        relationship_strength=extract_relation.relationship_strength,
        text_unit_ids=other.get("text_unit_ids", None),
        description_embedding=other.get("description_embedding", None),
    )
