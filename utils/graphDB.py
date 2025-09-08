from neo4j import GraphDatabase
from core.config import GraphConfig
from core.schema import Entity, Relation
from typing import List, Dict, Optional, Any, Union
import json


class graphDB:
    def __init__(self, config: GraphConfig):
        self.config = config
        self.graph = self._connect_to_database()
        if self.graph:
            print("连接成功！")
        else:
            raise ValueError("neo4j连接失败，请检查配置。")
    
    def _connect_to_database(self):
        """连接到Neo4j数据库"""
        try:
            driver = GraphDatabase.driver(
                self.config.neo4j_uri,
                auth=(self.config.neo4j_user, self.config.neo4j_password)
            )
            driver.verify_connectivity()
            return driver
        except Exception as e:
            print(f"连接失败: {e}")
            return None
    
    def close(self):
        """关闭数据库连接"""
        if self.graph:
            self.graph.close()
            print("数据库连接已关闭")
    
    def execute_query(self, query: str, parameters: Optional[Dict] = None) -> List[Dict]:
        """执行Cypher查询并返回结果"""
        try:
            with self.graph.session() as session:
                result = session.run(query, parameters or {})
                return [record.data() for record in result]
        except Exception as e:
            print(f"查询执行失败: {e}")
            return []
    
    # === 实体操作 ===
    
    def create_entity(self, entity: Entity) -> bool:
        """创建实体"""
        try:
            properties = {
                "entity_name": entity.entity_name,
                "entity_type": entity.entity_type,
                "entity_description": entity.entity_description
            }
            
            if entity.name_embedding:
                properties["name_embedding"] = entity.name_embedding
            
            if entity.description_embedding:
                properties["description_embedding"] = entity.description_embedding
            
            if entity.text_unit_ids:
                properties["text_unit_ids"] = entity.text_unit_ids
            
            query = """
            CREATE (n:Entity {entity_type: $entity_type})
            SET n += $properties
            RETURN n
            """
            
            result = self.execute_query(query, {
                "entity_type": entity.entity_type,
                "properties": properties
            })
            return len(result) > 0
        except Exception as e:
            print(f"创建实体失败: {e}")
            return False
    
    def find_entity(self, entity_name: str, entity_type: Optional[str] = None) -> List[Dict]:
        """查找实体"""
        try:
            if entity_type:
                query = """
                MATCH (n:Entity {entity_name: $entity_name, entity_type: $entity_type})
                RETURN n
                """
                return self.execute_query(query, {
                    "entity_name": entity_name,
                    "entity_type": entity_type
                })
            else:
                query = """
                MATCH (n:Entity {entity_name: $entity_name})
                RETURN n
                """
                return self.execute_query(query, {"entity_name": entity_name})
        except Exception as e:
            print(f"查找实体失败: {e}")
            return []
    
    def update_entity(self, entity_name: str, entity_type: str, update_data: Dict) -> bool:
        """更新实体"""
        try:
            query = """
            MATCH (n:Entity {entity_name: $entity_name, entity_type: $entity_type})
            SET n += $update_data
            RETURN n
            """
            
            result = self.execute_query(query, {
                "entity_name": entity_name,
                "entity_type": entity_type,
                "update_data": update_data
            })
            return len(result) > 0
        except Exception as e:
            print(f"更新实体失败: {e}")
            return False
    
    def delete_entity(self, entity_name: str, entity_type: Optional[str] = None) -> bool:
        """删除实体"""
        try:
            if entity_type:
                query = """
                MATCH (n:Entity {entity_name: $entity_name, entity_type: $entity_type})
                DETACH DELETE n
                """
                self.execute_query(query, {
                    "entity_name": entity_name,
                    "entity_type": entity_type
                })
            else:
                query = """
                MATCH (n:Entity {entity_name: $entity_name})
                DETACH DELETE n
                """
                self.execute_query(query, {"entity_name": entity_name})
            return True
        except Exception as e:
            print(f"删除实体失败: {e}")
            return False
    
    def get_all_entities(self, entity_type: Optional[str] = None) -> List[Dict]:
        """获取所有实体"""
        try:
            if entity_type:
                query = """
                MATCH (n:Entity {entity_type: $entity_type})
                RETURN n
                """
                return self.execute_query(query, {"entity_type": entity_type})
            else:
                query = """
                MATCH (n:Entity)
                RETURN n
                """
                return self.execute_query(query)
        except Exception as e:
            print(f"获取实体失败: {e}")
            return []
    
    # === 关系操作 ===
    
    def create_relation(self, relation: Relation) -> bool:
        """创建关系"""
        try:
            rel_properties = {
                "relationship_description": relation.relationship_description,
                "relationship_strength": relation.relationship_strength
            }
            
            if relation.description_embedding:
                rel_properties["description_embedding"] = relation.description_embedding
            
            if relation.text_unit_ids:
                rel_properties["text_unit_ids"] = relation.text_unit_ids
            
            if relation.weight:
                rel_properties["weight"] = relation.weight
            
            if relation.rank:
                rel_properties["rank"] = relation.rank
            
            query = """
            MATCH (a:Entity {entity_name: $source_entity})
            MATCH (b:Entity {entity_name: $target_entity})
            CREATE (a)-[r:RELATED_TO]->(b)
            SET r += $properties
            RETURN r
            """
            
            result = self.execute_query(query, {
                "source_entity": relation.source_entity,
                "target_entity": relation.target_entity,
                "properties": rel_properties
            })
            return len(result) > 0
        except Exception as e:
            print(f"创建关系失败: {e}")
            return False
    
    def find_relations(self, source_entity: Optional[str] = None, 
                      target_entity: Optional[str] = None) -> List[Dict]:
        """查找关系"""
        try:
            conditions = []
            params = {}
            
            if source_entity:
                conditions.append("a.entity_name = $source_entity")
                params["source_entity"] = source_entity
            
            if target_entity:
                conditions.append("b.entity_name = $target_entity")
                params["target_entity"] = target_entity
            
            where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
            
            query = f"""
            MATCH (a:Entity)-[r:RELATED_TO]->(b:Entity)
            {where_clause}
            RETURN a.entity_name as source_name, a.entity_type as source_type,
                   b.entity_name as target_name, b.entity_type as target_type,
                   r.relationship_description as relationship_description,
                   r.relationship_strength as relationship_strength,
                   r.description_embedding as description_embedding,
                   r.text_unit_ids as text_unit_ids,
                   r.weight as weight,
                   r.rank as rank
            """
            
            return self.execute_query(query, params)
        except Exception as e:
            print(f"查找关系失败: {e}")
            return []
    
    def update_relation(self, source_entity: str, target_entity: str, 
                       update_data: Dict) -> bool:
        """更新关系"""
        try:
            query = """
            MATCH (a:Entity {entity_name: $source_entity})-[r:RELATED_TO]->(b:Entity {entity_name: $target_entity})
            SET r += $update_data
            RETURN r
            """
            
            result = self.execute_query(query, {
                "source_entity": source_entity,
                "target_entity": target_entity,
                "update_data": update_data
            })
            return len(result) > 0
        except Exception as e:
            print(f"更新关系失败: {e}")
            return False
    
    def delete_relation(self, source_entity: str, target_entity: str) -> bool:
        """删除关系"""
        try:
            query = """
            MATCH (a:Entity {entity_name: $source_entity})-[r:RELATED_TO]->(b:Entity {entity_name: $target_entity})
            DELETE r
            """
            self.execute_query(query, {
                "source_entity": source_entity,
                "target_entity": target_entity
            })
            return True
        except Exception as e:
            print(f"删除关系失败: {e}")
            return False
    
    def get_all_relations(self) -> List[Dict]:
        """获取所有关系"""
        try:
            query = """
            MATCH (a:Entity)-[r:RELATED_TO]->(b:Entity)
            RETURN a.entity_name as source_name, a.entity_type as source_type,
                   b.entity_name as target_name, b.entity_type as target_type,
                   r.relationship_description as relationship_description,
                   r.relationship_strength as relationship_strength,
                   r.description_embedding as description_embedding,
                   r.text_unit_ids as text_unit_ids,
                   r.weight as weight,
                   r.rank as rank
            """
            return self.execute_query(query)
        except Exception as e:
            print(f"获取关系失败: {e}")
            return []
    
    # === 批量操作 ===
    
    def create_entities_batch(self, entities: List[Entity]) -> bool:
        """批量创建实体"""
        try:
            nodes = []
            for entity in entities:
                properties = {
                    "entity_name": entity.entity_name,
                    "entity_type": entity.entity_type,
                    "entity_description": entity.entity_description
                }
                
                if entity.name_embedding:
                    properties["name_embedding"] = entity.name_embedding
                
                if entity.description_embedding:
                    properties["description_embedding"] = entity.description_embedding
                
                if entity.text_unit_ids:
                    properties["text_unit_ids"] = entity.text_unit_ids
                
                nodes.append(properties)
            
            query = """
            UNWIND $entities AS entity
            CREATE (n:Entity {entity_type: entity.entity_type})
            SET n += entity
            RETURN count(n) as created
            """
            
            result = self.execute_query(query, {"entities": nodes})
            return len(result) > 0
        except Exception as e:
            print(f"批量创建实体失败: {e}")
            return False
    
    def create_relations_batch(self, relations: List[Relation]) -> bool:
        """批量创建关系"""
        try:
            rels = []
            for relation in relations:
                rel_properties = {
                    "source_entity": relation.source_entity,
                    "target_entity": relation.target_entity,
                    "relationship_description": relation.relationship_description,
                    "relationship_strength": relation.relationship_strength
                }
                
                if relation.description_embedding:
                    rel_properties["description_embedding"] = relation.description_embedding
                
                if relation.text_unit_ids:
                    rel_properties["text_unit_ids"] = relation.text_unit_ids
                
                if relation.weight:
                    rel_properties["weight"] = relation.weight
                
                if relation.rank:
                    rel_properties["rank"] = relation.rank
                
                rels.append(rel_properties)
            
            query = """
            UNWIND $relations AS rel
            MATCH (a:Entity {entity_name: rel.source_entity})
            MATCH (b:Entity {entity_name: rel.target_entity})
            CREATE (a)-[r:RELATED_TO]->(b)
            SET r += rel
            RETURN count(r) as created
            """
            
            result = self.execute_query(query, {"relations": rels})
            return len(result) > 0
        except Exception as e:
            print(f"批量创建关系失败: {e}")
            return False
    
    # === 数据导入导出 ===
    
    def import_from_json(self, file_path: str) -> bool:
        """从JSON文件导入数据"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'entities' in data:
                entities = []
                for entity_data in data['entities']:
                    entity = Entity(
                        entity_name=entity_data.get('entity_name'),
                        entity_type=entity_data.get('entity_type'),
                        entity_description=entity_data.get('entity_description'),
                        name_embedding=entity_data.get('name_embedding'),
                        description_embedding=entity_data.get('description_embedding'),
                        text_unit_ids=entity_data.get('text_unit_ids')
                    )
                    entities.append(entity)
                
                self.create_entities_batch(entities)
            
            if 'relations' in data:
                relations = []
                for relation_data in data['relations']:
                    relation = Relation(
                        source_entity=relation_data.get('source_entity'),
                        target_entity=relation_data.get('target_entity'),
                        relationship_description=relation_data.get('relationship_description'),
                        relationship_strength=relation_data.get('relationship_strength'),
                        description_embedding=relation_data.get('description_embedding'),
                        text_unit_ids=relation_data.get('text_unit_ids'),
                        weight=relation_data.get('weight'),
                        rank=relation_data.get('rank')
                    )
                    relations.append(relation)
                
                self.create_relations_batch(relations)
            
            return True
        except Exception as e:
            print(f"导入失败: {e}")
            return False
    
    def export_to_json(self, file_path: str) -> bool:
        """导出数据到JSON文件"""
        try:
            data = {
                'entities': [],
                'relations': []
            }
            
            # 导出实体
            entities = self.get_all_entities()
            for entity in entities:
                entity_props = entity.get('n', {})
                data['entities'].append({
                    'entity_name': entity_props.get('entity_name'),
                    'entity_type': entity_props.get('entity_type'),
                    'entity_description': entity_props.get('entity_description'),
                    'name_embedding': entity_props.get('name_embedding'),
                    'description_embedding': entity_props.get('description_embedding'),
                    'text_unit_ids': entity_props.get('text_unit_ids')
                })
            
            # 导出关系
            relations = self.get_all_relations()
            for rel in relations:
                data['relations'].append({
                    'source_entity': rel.get('source_name'),
                    'target_entity': rel.get('target_name'),
                    'relationship_description': rel.get('relationship_description'),
                    'relationship_strength': rel.get('relationship_strength'),
                    'description_embedding': rel.get('description_embedding'),
                    'text_unit_ids': rel.get('text_unit_ids'),
                    'weight': rel.get('weight'),
                    'rank': rel.get('rank')
                })
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"导出失败: {e}")
            return False
    
    # === 清空数据库 ===
    
    def clear_database(self) -> bool:
        """清空数据库"""
        try:
            query = "MATCH (n) DETACH DELETE n"
            self.execute_query(query)
            return True
        except Exception as e:
            print(f"清空数据库失败: {e}")
            return False