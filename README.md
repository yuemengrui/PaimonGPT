# PaimonGPT

[GO! 看文档去～](https://yuemengrui.gitbook.io/paimongpt "GO! 看文档去～")

# 介绍

大模型时代，人人都在探索大模型该如何落地。RAG是一条最火，最简单(bushi😆)
的实现方式。出一个demo很简单，效果看着还可以，但实际落地时，却一大堆问题：检索的内容不准确、大模型的回答乱发散等等。
本项目完成了一套完整的RAG流程，可直接部署使用。

# 项目架构

![image](https://github.com/yuemengrui/PaimonGPT/blob/main/assets/images/PaimonGPT架构.png?raw=true)  
本项目分成好几个模块：
- 后台服务：为PaimonGPT的主体后台服务
- 前端：提供一个前端可供开箱使用
- Embedding Server: 顾名思义, 提供embedding的服务。通过模型注册接口注册到后台服务中，方便插拔。
- LLM Server: 顾名思义，提供大模型的服务。通过模型注册接口注册到后台服务中，方便插拔。
- 版面分析服务：提供PDF的版面分析能力。
- 分词服务：提供分词的能力，主要用于BM25Retriever。
- OCR服务：提供OCR能力。
- Others Servers: 未来可能会有的一些其他能力的集成。

# RAG架构

![image](https://github.com/yuemengrui/PaimonGPT/blob/main/assets/images/RAG.png?raw=true)  
1.整体流程  
用户上传文档，文档通过文档加载器切分成chunks，此时的chunks相较大，通常是一段文本，描述某一项内容。然后再次将parent chunks 切分成child chunks，将child chunks存入Vector DB。用户提问，问题经过检索器模块，检索器模块中包含多种检索器，每种检索器都将检索到与用户问题相关的child chunks，再经过一个RRF模块，对检索到的chunks进行排序，通过child chunks 关联到parent chunks， 将parent chunks 根据大模型最大token长度选择合适的chunks, 将这些chunks组装成prompt送入大模型，大模型给出回答。  

2.文档加载器(document loader)  
支持主流的文件类型，如TXT、MD、Word等等。特别针对PDF文件添加版面分析模块。可以更好的切分PDF文件。  

3.Parent Chunks 与 Child Chunks  
文本切分是一个比较麻烦的问题，切的太碎了，检索出来的内容缺少详细上下文，大模型的回答依然不太理想。切的太大了，embedding检索效果不理想，context过长也会超出大模型的最大token长度。  

4.检索器(Retrievers)  
目前有两种检索器：  
MultiQueryRetriever：该检索器主要用于query改写。很多时候用户的问题并不是特别明确，如果直接拿问题去向量库检索，效果可能并不好，通过原始query生成多个相似query，然后再去向量库检索，检索效果会有显著的改善。  
BM25Retriever：该检索器的主要作用是提高召回率，弥补向量检索会遗漏的内容。BM25检索器通过关键词检索，但有的时候用户的问题中的关键词可能并不是文档中的关键词，可能是口语化的关键词或者同义词等等，直接检索效果并不理想。这里引入分词模型，分词更加精准。引入同义词推荐模型，根据用户问题中的关键词推荐同义的一些关键词，可以显著提高召回率。同时针对特定领域，会存在很多领域的专有名词，增加一个领域词库，可以配置领域专有名词，同时配置该词的同义词、不同说法的词。还可以给关键词打上标签。比如我的知识库中有两篇文档，一篇讲transformer架构，一篇讲大模型，用户问：AI相关的算法有哪些？但是两篇文档中都未出现‘AI’这个关键词，直接检索的话可能结果不理想，通过给transformer、大模型打上AI的标签，可以显著提高召回率。  
未来还会添加新的检索器。  

5.RRF(倒数索引排序)  
可对各个检索器检索出来的内容进行rerank，提高检索精度。  

# 部署

1. 拉取源代码
```commandline
git clone https://github.com/yuemengrui/PaimonGPT.git
```

2. 进入目录 
```commandline
cd PaimonGPT
```

3. 拉取 分词服务 源代码 
```commandline
git clone https://github.com/yuemengrui/AI_Tokenizer_Server.git
```

4. 拉取 embedding服务 源代码  
```commandline
git clone https://github.com/yuemengrui/Embedding_Server.git
```
   
5. 拉取 版面分析 源代码  
```commandline
git clone https://github.com/yuemengrui/AI_Tools_Servers.git
```
   
6. 拉取 大模型部署服务 源代码  
```commandline
git clone https://github.com/yuemengrui/LMCenter.git
```
在LMCenter/ModelWorker/configs/目录下创建一个新的配置文件，例如baichuan2_13b_configs.py, 可从configs.py.template复制一份，修改相关配置项, 只需修改ModelWorkerConfig中的部分配置项即可
```commandline
########################

ModelWorkerConfig = {
    "controller_addr": "http://model_controller:24620",  // controller地址
    "worker_addr": f"http://xxx:{FASTAPI_PORT}", // worker地址，将xxx替换为你的容器名
    "worker_id": WORKER_ID,
    "worker_type": "",  # vllm or others // worker类型，可以选择是否启用vllm
    "model_type": "xx",  # ['Baichuan', 'ChatGLM3', 'Qwen2']  // 支持的模型类型
    "model_path": "xxx",  // 模型路径，为上面docker-compose.yml中挂载的模型文件夹, 例如：/workspace/Models/Baichuan2-13B-Chat
    "model_name": "xxx",  // 模型名
    "limit_worker_concurrency": 5,
    "multimodal": False,  // 是否是多模态模型
    "device": "cuda",
    "dtype": "float16",  # ["float32", "float16", "bfloat16"], // 模型精度，推荐bfloat16
    "gpu_memory_utilization": 0.9
}


########################
```
![image](https://github.com/yuemengrui/PaimonGPT/blob/main/assets/images/deploy_1.png?raw=true)
说明：DATA目录为存放项目一些使用数据的目录，其中的DATA/Models目录存放项目用到的models。   
我将分词模型放在了[谷歌云盘](https://drive.google.com/file/d/1SBYephGXV20bpDG3XQ3lp7SEW_XgWlHq/view?usp=share_link)上，需要的可以自行下载。  
![image](https://github.com/yuemengrui/PaimonGPT/blob/main/assets/images/deploy_2.png?raw=true)

上述步骤都准备好时，直接在docker_compose.yml同级目录中，
修改docker_compose.yml中的一些配置项，主要修改GPU卡的使用

vim docker_compose.yml

```commandline
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          device_ids: [ "0" ]
          capabilities: [ gpu ]
```

在一些需要使用GPU的服务中会有上面这个GPU的配置。
其他模型包括：OCR、版面分析模型、分词模型、bge embedding模型，这些模型加起来大概8G显存

如果你是docker大佬，也可以随意修改你想修改的地方

上面的都准备好了之后，激动人心的时候终于来了，开始启动服务  
```commandline
sudo docker compose up -d
```  

静待5分钟, 查看服务健康情况, 不出意外的话，所有服务应该是(healthy)的状态  
```commandline
sudo docker compose ps
```
![image](https://github.com/yuemengrui/PaimonGPT/blob/main/assets/images/deploy_3.png?raw=true)
启动成功后，浏览器访问 ‘你的ip:24600’ 即可体验PaimonGPT

![image](https://github.com/yuemengrui/PaimonGPT/blob/main/assets/images/paimongpt_1.png?raw=true)

# 相关项目
- [PaimonGPT-UI](https://github.com/yuemengrui/PaimonGPT-UI.git) PaimonGPT的前端项目，使用Next.js react编写。
- [AI_Tokenizer_Server](https://github.com/yuemengrui/AI_Tokenizer_Server.git) 分词服务，主要用于分词。
- [AI_Tools_Servers](https://github.com/yuemengrui/AI_Tools_Servers.git) 其实是一些工具类的服务会放在这里，目前只放了一个版面分析的服务，未来可能会添加一些其他的服务。
- [Embedding_Server](https://github.com/yuemengrui/Embedding_Server.git) 就是Embedding啦，都是用sentence_transformers加载的模型
- [LMCenter](https://github.com/yuemengrui/LMCenter.git) 大模型部署的服务，主要用于部署大模型，提供大模型的服务。

