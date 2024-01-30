# *_*coding:utf-8 *_*
# @Author : YueMengRui
""
kb_qa_prompt_template = """你是一个出色的文档问答助手，根据参考材料来回答用户的问题，仔细分析和思考参考材料与用户问题之间的关系，忽略你认为与用户问题无关的材料，回答要合理、简洁，直接回复答案，回复语言采用中文。
用户的问题是：{query}
参考材料：
```
{context}
```
"""

# context:
# 文本片段1: xxx
# 文本片段2: xxx

"""你是文字提取器，你要结构化的提取用户描述中的年份、省、市信息,没有年份、省、市信息信息则使用空值("")代替。
年份 (year) 指：用户输入中有含义的年份信息，如：2022、2021、""等
省 (province)：用户输入中有含义的省一级信息，如：云南省、山西省、""等
市(city)：用户输入中有含义的市一级信息，如：昆明市、成都市、""等
只能输出JSON格式，输出完毕后结束，不要生成新的用户输入，不要增加额外内容

示例：
用户输入：2022年上海市蝗虫的发生情况。
json: {"year" : "2022", "province":"上海市", "city": "上海市"}

用户输入：2022年昆明市病虫情报第1期。
json: {"year":"2022", "province":"云南省", "city"："昆明市"}

用户输入：蝗虫的发生情况。
json: {"year":"", "province":"", "city": ""}

请根据以下文本，按照模版输出内容。
用户输入：2022年昆明市小春粮食作物的情况
"""

"""
你是一个出色的助手，你需要判断给定的文本片段和用户的问题之间的关联性，仔细分析和思考用户的问题和下面每个文本片段的内容，将文本片段按照与问题的关联性从高到低重新排序，并去掉你认为不相关的文本片段，只返回排序后的文本片段列表。
用户的问题是：{query}
文本片段列表：
```
{context}
```
"""

"""
这是一个文本纠错任务，找出并纠正给定文本中的错误，如错字、错词等等，只返回纠正后的文本。
给定文本：{query}
"""

multiqueryretriever_prompt_template = """
问句：{query}。
分析上面的问句，从多种角度生成最多3个相似问句。
使用 json 格式回答，确保你的回答必须是正确的 json 格式，并且能被 python 语言的 `json.loads` 库解析。
"""

tableQA_prompt_template = """
你是一个专业的表格数据分析师。根据给定的表格数据来回答用户的问题。
用户的问题是：{query}
表格数据是：
{context}
"""

DBQA_PROMPT_TEMPLATE = """你是一个 SQL 专家，给你一个用户的问题，你会生成一条对应的 mysql 语法的 SQL 语句。

注意：
1. 如果用户没有在问题中指定 sql 返回多少条数据，那么你生成的 sql 最多返回 {top_k} 条数据。
2. 你应该尽可能少地使用表。
3. 只能使用表结构信息中提供的表来生成 sql，如果无法根据提供的表结构中生成 sql ，请说：“提供的表结构信息不足以生成 sql 查询。” 禁止随意捏造信息。
4. 不要查询不存在的列，注意哪一列位于哪张表中。
5. 不要返回你的思考过程，直接返回sql语句。使用 json 格式回答，确保你的回答是必须是正确的 json 格式，并且能被 python 语言的 `json.loads` 库解析, 格式如下：
{{"sql": "你生成的sql"}} 

这是几个示例：{examples}

用户的问题是：{query}
已知表结构信息如下：
{table_info}"""
