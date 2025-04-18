from camel.agents import ChatAgent
from camel.models import ModelFactory
from camel.types import ModelPlatformType
from camel.messages import BaseMessage
from camel.societies.workforce import Workforce
from camel.toolkits import SearchToolkit
from camel.tasks import Task
from camel.toolkits import FunctionTool
from dotenv import load_dotenv
import os
from pathlib import Path

# 获取当前脚本的绝对路径
print("系统原生环境变量:", os.environ.get('QWEN_API_KEY'))
current_script_path = Path(__file__).resolve()

# 方案一：显式指定 .env 路径（推荐）
env_path = current_script_path.parent / ".env"  # 假设 .env 在代码所在目录
load_dotenv(dotenv_path=env_path,override=True)
api_key = os.getenv('QWEN_API_KEY')
model = ModelFactory.create(
    model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
    model_type="Qwen/Qwen2.5-72B-Instruct",
    url='https://api-inference.modelscope.cn/v1/',
    api_key=api_key,
    model_config_dict={"temperature": 0.4, "max_tokens": 4096},
)
'''
api_key = os.getenv('GEMINI_API_KEY')
base_url=os.getenv('BASE_URL_GEMINI')
chat_model=os.getenv('CHAT_MODEL_GEMINI')

model = ModelFactory.create(
    model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
    model_type=chat_model,
    url=base_url,
    api_key=api_key
)

api_key = os.getenv('ONE_API_KEYK')
model = ModelFactory.create(
    model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
    model_type="gemini-2.5-pro-exp-03-25",
    url='https://wilful-cicily-zhongdadianzi-8b661d5f.koyeb.app/v1/',
    api_key=api_key,
    model_config_dict={"temperature": 0, "max_tokens": 8096},
)
'''
# 创建一个 Workforce 实例
workforce = Workforce(description="旅游攻略制作与评估工作组",new_worker_agent_kwargs={'model':model},coordinator_agent_kwargs={'model':model},task_agent_kwargs={'model':model})
search_tool = FunctionTool(SearchToolkit().search_duckduckgo)

search_agent = ChatAgent(
            system_message="""你是一个专业的旅游信息搜索助手。你的职责是:
                1. 搜索目的地的主要景点信息
                2. 搜索当地特色美食信息
                3. 搜索交通和住宿相关信息
                请确保信息的准确性和实用性。""",
            model=model,
            tools=[search_tool],
            output_language='中文'
        )

planner_agent = ChatAgent(
            system_message="""你是一个专业的旅行规划师。你的职责是:
                1. 根据景点分布规划合理的游览顺序
                2. 为每天安排适量的景点和活动
                3. 考虑用餐、休息等时间
                4. 注意不同季节的特点
                请确保行程安排合理且具有可行性。""",
            model=model,
            output_language='中文'
        )

reviewer_agent = ChatAgent(
    system_message="""你是一个经验丰富的旅行爱好者。你的职责是:
        1. 从游客角度评估行程的合理性
        2. 指出可能的问题和改进建议
        3. 补充实用的旅行小贴士
        4. 评估行程的性价比
        请基于实际旅行经验给出中肯的建议。""",
    model=model,
    output_language='中文'
)
# 添加一个执行网页搜索的Agent
workforce.add_single_agent_worker(
    "一个能够执行网页搜索的Agent",    worker=search_agent,
)# 添加工作节点
workforce.add_single_agent_worker(
    "负责搜索目的地相关信息",
    worker=search_agent
).add_single_agent_worker(
    "负责制定详细行程规划",
    worker=planner_agent
).add_single_agent_worker(
    "负责从游客角度评估行程",
    worker=reviewer_agent
)
from camel.tasks import Task

# 创建一个用于测试的任务
task = Task(
    content="规划一个3天的巴黎旅行计划。",
    id="0",  # id可以是任何标记字符串
)
# 使用jupyter来运行代码请打开下面两行注释
# import nest_asyncio
# nest_asyncio.apply()


# 让 Workforce 处理这个任务
task = workforce.process_task(task)
print(task.result)