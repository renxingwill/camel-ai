# CAMEL-AI 代码使用说明

本文档提供了 CAMEL-AI 框架相关代码的使用说明，帮助您理解和运行目录中的各个 Python 文件。

## 环境准备

在运行代码前，请确保已安装所需的依赖。您可以通过以下两种方式安装依赖：

### 方式一：使用 requirements.txt 一键安装所有依赖

```bash
pip install -r requirements.txt
```

### 方式二：手动安装各个依赖

```bash
pip install camel-ai python-dotenv colorama pillow requests sentence-transformers
# 对于rag_1.py，还需要安装
pip install python-magic-bin
```

## API 密钥配置

大多数代码示例需要使用大语言模型 API，请在项目根目录创建`.env`文件，并配置以下 API 密钥：

```
QWEN_API_KEY=your_qwen_api_key
ZHIPUAI_API_KEY=your_zhipu_api_key
ZHIPUAI_API_BASE_URL=your_zhipu_api_base_url
# 可选的其他API密钥
GEMINI_API_KEY=your_gemini_api_key
BASE_URL_GEMINI=your_gemini_base_url
CHAT_MODEL_GEMINI=your_gemini_model_name
```

## 代码文件说明

### 1. role.py - 角色扮演对话

这个文件演示了 CAMEL 框架的角色扮演功能，创建了一个 AI 助手和 AI 用户之间的对话，共同完成特定任务。

**主要功能：**

- 使用智谱 AI 的 GLM-4 模型
- 设置 AI 助手角色（Python 程序员）和 AI 用户角色（股票交易员）
- 定义任务目标（开发股票交易机器人）
- 支持中文输出

**使用方法：**

```bash
python role.py
```

### 2. workforce.py - 多智能体工作流

这个文件展示了如何创建一个多智能体工作组，协同完成复杂任务。

**主要功能：**

- 创建旅游攻略制作与评估工作组
- 包含三个专业智能体：搜索助手、旅行规划师和评估者
- 使用通义千问大模型
- 集成搜索工具

**使用方法：**

```bash
python workforce.py
```

### 3. chat_agent_tool.py - 工具增强型对话智能体

这个文件演示了如何创建具有工具调用能力的对话智能体。

**主要功能：**

- 创建基础对话智能体
- 定义和使用自定义工具函数
- 展示工具调用过程
- 结合搜索和数学工具包进行角色扮演

**使用方法：**

```bash
python chat_agent_tool.py
```

### 4. chat_memory_vector.py - 向量记忆增强对话

这个文件展示了如何使用向量数据库增强智能体的记忆能力。

**主要功能：**

- 创建向量数据库记忆块
- 存储和检索对话记录
- 使用长期记忆系统
- 基于上下文的智能体对话

**使用方法：**

```bash
python chat_memory_vector.py
```

### 5. message_image.py - 多模态消息处理

这个文件演示了如何处理包含图像的多模态消息。

**主要功能：**

- 创建包含图像的用户消息
- 使用多模态模型处理图像
- 转换消息格式
- 展示 ChatAgent 对图像的描述能力

**使用方法：**

```bash
python message_image.py
```

### 6. rag_1.py - 检索增强生成

这个文件展示了如何实现检索增强生成(RAG)系统。

**主要功能：**

- 使用向量检索器和 BM25 检索器
- 创建和使用向量数据库存储
- 文本分块和嵌入
- 基于检索结果生成回答

**使用前准备：**

1. 创建`local_data`目录
2. 在该目录中放入名为`网红.txt`的文本文件

**使用方法：**

```bash
python rag_1.py
```

## 注意事项

1. 部分代码使用了在线模型，需要确保网络连接正常
2. 对于嵌入模型，如果无法在线下载，可以使用代码中注释的离线方案
3. 运行 rag_1.py 前，请确保已创建所需的文件和目录
4. 如果使用 Jupyter Notebook 运行 workforce.py，请取消注释相关代码

## 更多资源

- CAMEL-AI 官方文档：[https://github.com/camel-ai/camel](https://github.com/camel-ai/camel)
- 嵌入模型下载：[https://hf-mirror.com/intfloat/e5-large-v2/tree/main](https://hf-mirror.com/intfloat/e5-large-v2/tree/main)
