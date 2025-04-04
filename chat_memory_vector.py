from camel.memories.blocks.vectordb_block import VectorDBBlock
from camel.memories.records import MemoryRecord
from camel.messages import BaseMessage
from camel.embeddings import SentenceTransformerEncoder
from camel.types import OpenAIBackendRole
from dotenv import load_dotenv
import os

load_dotenv()
#os.environ["HF_HOME"] = "./models"
# 创建一个 VectorDBBlock 实例
vector_db_block = VectorDBBlock(embedding=SentenceTransformerEncoder(model_name="intfloat/e5-large-v2"))

# 创建一些示例聊天记录
records = [
    MemoryRecord(message=BaseMessage.make_user_message(role_name="user", content="今天天气真好！"), role_at_backend=OpenAIBackendRole.USER),
    MemoryRecord(message=BaseMessage.make_user_message(role_name="user", content="你喜欢什么运动？"), role_at_backend=OpenAIBackendRole.USER),
    MemoryRecord(message=BaseMessage.make_user_message(role_name="user", content="今天天气不错，我们去散步吧。"), role_at_backend=OpenAIBackendRole.USER),
]

# 将记录写入向量数据库
vector_db_block.write_records(records)

# 使用关键词进行检索
keyword = "天气"
retrieved_records = vector_db_block.retrieve(keyword=keyword, limit=3)

for record in retrieved_records:
    print(f"UUID: {record.memory_record.uuid}, Message: {record.memory_record.message.content}, Score: {record.score}")
from camel.memories import (
    LongtermAgentMemory,
    MemoryRecord,
    ScoreBasedContextCreator,
    ChatHistoryBlock,
    VectorDBBlock,
)
from camel.messages import BaseMessage
from camel.types import ModelType, OpenAIBackendRole
from camel.utils import OpenAITokenCounter
from camel.embeddings import SentenceTransformerEncoder

# 1. 初始化内存系统
memory = LongtermAgentMemory(
    context_creator=ScoreBasedContextCreator(
        token_counter=OpenAITokenCounter(ModelType.GPT_4O_MINI),
        token_limit=1024,
    ),
    chat_history_block=ChatHistoryBlock(),
    vector_db_block=VectorDBBlock(embedding=SentenceTransformerEncoder(model_name="intfloat/e5-large-v2")),
)

# 2. 创建记忆记录
records = [
    MemoryRecord(
        message=BaseMessage.make_user_message(
            role_name="User",
            content="什么是CAMEL AI?"
        ),
        role_at_backend=OpenAIBackendRole.USER,
    ),
    MemoryRecord(
        message=BaseMessage.make_assistant_message(
            role_name="Agent",
            content="CAMEL-AI是第一个LLM多智能体框架,并且是一个致力于寻找智能体 scaling law 的开源社区。"
        ),
        role_at_backend=OpenAIBackendRole.ASSISTANT,
    ),
]

# 3. 写入记忆
memory.write_records(records)

context, token_count = memory.get_context()

print(context)
print(f'token消耗: {token_count}')

from camel.agents import ChatAgent
from camel.models import ModelFactory
from camel.types import ModelPlatformType
import os
from dotenv import load_dotenv

load_dotenv()
# 定义系统消息
sys_msg = "你是一个好奇的智能体，正在探索宇宙的奥秘。"

# 初始化agent 调用在线Qwen/Qwen2.5-72B-Instruct
api_key = os.getenv('QWEN_API_KEY')

model = ModelFactory.create(
    model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
    model_type="Qwen/Qwen2.5-72B-Instruct",
    url='https://api-inference.modelscope.cn/v1/',
    api_key=api_key
)
agent = ChatAgent(system_message=sys_msg, model=model)

# 定义用户消息
usr_msg = "告诉我基于我们讨论的内容，哪个是第一个LLM多智能体框架？"

# 发送消息给agent
response = agent.step(usr_msg)

# 查看响应
print(response.msgs[0].content)
# 将memory赋值给agent
agent.memory = memory
# 发送消息给agent
response = agent.step(usr_msg)
# 查看响应
print(response.msgs[0].content)

