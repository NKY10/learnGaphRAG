from langchain_core.prompts import PromptTemplate

extract_prompt = PromptTemplate(
    template='''
    ## 任务
    请你担任一名专业的知识提取和组织专家，任务是从给定的文本中提取实体关系信息及其描述，用于构建知识图谱
    ## 输出格式
    按照LLMOutput的格式组织。
    ## 要求
    实体类型包括：人物、组织、地点、事件、概念等。
    关系类型包括：人物之间的关系、组织之间的关系、地点之间的关系、事件之间的关系、概念之间的关系等。
    关系描述中包含关系的强度、方向等信息。
    ## 注意：
    1. 实体描述中是对实体自身的描述，不能包含关系描述。
    2. 关系描述中是对实体之间的关系描述，而不是实体的信息。
    文本内容：{text}
    ''',
    input_variables=["text"]
)


