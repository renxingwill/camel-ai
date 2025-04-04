
#先执行这个pip install python-magic-bin
import os
import requests
from pathlib import Path

'''
os.makedirs('local_data', exist_ok=True)
url = "https://arxiv.org/pdf/2303.17760.pdf"
response = requests.get(url)
with open('local_data/camel_paper.pdf', 'wb') as file:
    file.write(response.content)
'''
from dotenv import load_dotenv
import os

# 获取当前脚本的绝对路径
print("系统原生环境变量:", os.environ.get('QWEN_API_KEY'))
current_script_path = Path(__file__).resolve()

# 方案一：显式指定 .env 路径（推荐）
env_path = current_script_path.parent / ".env"  # 假设 .env 在代码所在目录
load_dotenv(dotenv_path=env_path,override=True)
api_key = os.getenv('QWEN_API_KEY')
print(api_key)
from camel.retrievers import VectorRetriever
from camel.retrievers import BM25Retriever
from camel.types import StorageType
from camel.embeddings import SentenceTransformerEncoder

embedding_model=SentenceTransformerEncoder(model_name='intfloat/e5-large-v2')

# 国内无法运行上述代码，可以注释掉使用以下方案
# embedding_model=SentenceTransformerEncoder(model_name='./embedding_model/')
# 下载方案2：打开这个链接https://hf-mirror.com/intfloat/e5-large-v2/tree/main，下载除了model.safetensors的以外部分，保存到当前代码同级目录的embedding_model文件夹下。
# 也可以从百度云盘直接下载embedding_model文件夹放到当前代码同级目录下。
# https://pan.baidu.com/s/1xt0Tg_Wmr8iJuyGiPfgJrw 提取码: 7pzr 

# 初始化VectorRetriever实例并使用本地模型作为嵌入模型
vr = VectorRetriever(embedding_model= embedding_model)
br = BM25Retriever()
# 创建并初始化一个向量数据库 (以QdrantStorage为例)
from camel.storages.vectordb_storages import QdrantStorage
# 确保PDF能正确解析

vector_storage = QdrantStorage(
    vector_dim=embedding_model.get_output_dim(),
    collection="demo_collection",
    path="storage_customized_run",
    collection_name="论文"
)

vr = VectorRetriever(embedding_model= embedding_model,storage=vector_storage)
# 将文件读取、切块、嵌入并储存在向量数据库中
'''
from PyPDF2 import PdfReader
reader = PdfReader("local_data/camel_paper.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"
if not text.strip():
    raise ValueError("PDF内容为空或解析失败！")
# 处理文件时指定分块参数
'''
from pathlib import Path

import os
from pathlib import Path

# 获取当前脚本所在目录
current_dir = Path(__file__).parent
file_path = current_dir / "local_data" / "网红.txt"

# 打印调试信息
print(f"当前工作目录: {os.getcwd()}")
print(f"尝试访问的绝对路径: {file_path.resolve()}")
print(f"文件是否存在: {file_path.exists()}")

# 安全读取文件内容（带异常处理）
try:
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
        print(f"成功读取文件，字符数：{len(text)}")  # 验证读取成功
except Exception as e:
    print(f"文件读取失败: {str(e)}")
    raise
vr.process(
    content=text,
    storage=vector_storage,
    chunk_size=500,
    chunk_overlap=50
)

# 检查向量存储条目数（假设QdrantStorage支持count方法）
import os
print("存储路径是否存在:", os.path.exists("storage_customized_run"))

query = "CAMEL是什么"

# 执行查询并获取结果
results = vr.query(query=query, top_k=1)
print('results：',results)
from camel.agents import ChatAgent
from camel.models import ModelFactory
from camel.types import ModelPlatformType

retrieved_info_irrevelant = vr.query(
    query="如何延长网红周期",
    top_k=3,
    similarity_threshold=0.6
)
retrieved_info_irrevelant1 = vr.query(
    query="为什么网红会有周期?",
    top_k=2,
)

assistant_sys_msg = """
你是一个帮助回答问题的助手，
我会给你原始查询和检索到的上下文，
根据检索到的上下文回答原始查询，
如果你无法回答问题就说我不知道。
"""

model = ModelFactory.create(
        model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
        model_type="Qwen/Qwen2.5-72B-Instruct",
        url='https://api-inference.modelscope.cn/v1/',
        api_key= api_key
    )

# 将之前的retrieved_info转换为字符串形式
user_msg = str(retrieved_info_irrevelant)
print('usermsg：',user_msg)
user_msg1 = str(retrieved_info_irrevelant1)
print('usermsg1：',user_msg1)
agent = ChatAgent(assistant_sys_msg,model=model)
# 使用step方法获得最终的检索增强生成的回复并打印
assistant_response = agent.step(user_msg)
print(assistant_response.msg.content)