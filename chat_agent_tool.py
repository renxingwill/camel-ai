from camel.agents import ChatAgent
from camel.models import ModelFactory
from camel.types import ModelPlatformType
from camel.messages import BaseMessage
from camel.toolkits import FunctionTool
import os
from dotenv import load_dotenv
import time
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
# 创建模型
model = ModelFactory.create(
    model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
    model_type="Qwen/Qwen2.5-72B-Instruct",
    url='https://api-inference.modelscope.cn/v1/',
    api_key=api_key,
    model_config_dict={"temperature": 0.4, "max_tokens": 4096},
)
'''
model = ModelFactory.create(
    model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
    model_type="gemini-2.0-pro-exp-02-05", #gemini-2.0-flash-exp
    url='https://generativelanguage.googleapis.com/v1beta/openai/',
    api_key=api_key
)
agent = ChatAgent(system_message=sys_msg, model=model,output_language='中文')
# 定义系统消息
sys_msg = "你是一个数学大师，擅长各种数学问题。"
# 定义用户消息
usr_msg = "19987*2133等于多少？"
# 发送消息给agent
response = agent.step(usr_msg)
print(response.msgs[0].content)


def add(a: int, b: int) -> int:
    r"""将两个数字相乘。

Args:
    a (int): The first number to be multiplied.
    b (int): The second number to be multiplied.

Returns:
    integer: The product of the two numbers.
    """
    return a * b

# 用 FunctionTool 包装该函数
add_tool = FunctionTool(add)
print(add_tool.get_function_name())
print(add_tool.get_function_description())
# 定义系统消息
sys_msg = "你是一个数学大师，擅长各种数学问题。当你遇到数学问题的时候，你要调用工具，将工具计算的结果作为答案"

tool_agent = ChatAgent(
    tools = [add_tool],
    system_message=sys_msg,
    model=model,
    output_language="中文")
    
# 重新发送消息给toolagent
response = tool_agent.step(usr_msg)
print(response.msgs[0].content)
print(response.info['tool_calls'])
'''
# 定义系统消息
sys_msg = "你是一个数学大师，擅长各种数学问题。"
agent = ChatAgent(system_message=sys_msg, model=model,output_language='中文')

# 定义用户消息
usr_msg = "19987*2133等于多少？"
# 发送消息给agent
response = agent.step(usr_msg)
print(response.msgs[0].content)


def add(a: int, b: int) -> int:
    r"""将两个数字相乘。

Args:
    a (int): The first number to be multiplied.
    b (int): The second number to be multiplied.

Returns:
    integer: The product of the two numbers.
    """
    return a * b

# 用 FunctionTool 包装该函数
add_tool = FunctionTool(add)
print(add_tool.get_function_name())
print(add_tool.get_function_description())
# 定义系统消息
sys_msg = "你是一个数学大师，擅长各种数学问题。当你遇到数学问题的时候，你要调用工具，将工具计算的结果作为答案"

tool_agent = ChatAgent(
    tools = [add_tool],
    system_message=sys_msg,
    model=model,
    output_language="中文")
    
# 重新发送消息给toolagent
response = tool_agent.step(usr_msg)
print(response.msgs[0].content)
print(response.info['tool_calls'])
from camel.toolkits import SearchToolkit,MathToolkit
from camel.models import ModelFactory
from camel.types import ModelPlatformType
from camel.societies import RolePlaying
from camel.utils import print_text_animated
from colorama import Fore

import os

# 设置代理
#os.environ["http_proxy"] = "http://127.0.0.1:7897"
#os.environ["https_proxy"] = "http://127.0.0.1:7897"

#定义工具包
tools_list = [
    *SearchToolkit().get_tools(),
    *MathToolkit().get_tools()
]

# 设置任务
task_prompt = ("假设现在是2024年，"
        "牛津大学的成立年份，并计算出其当前年龄。"
        "然后再将这个年龄加上10年。使用谷歌搜索工具。")
        
#如果没有谷歌搜索API，可以使用duckduckgo工具，无需设置api即可使用        
# task_prompt = ("假设现在是2024年，"
#         "牛津大学的成立年份，并计算出其当前年龄。"
#         "然后再将这个年龄加上10年。使用duckduckgo搜索工具。")



# 设置角色扮演
role_play_session = RolePlaying(
    assistant_role_name="搜索者",
    user_role_name="教授",
    assistant_agent_kwargs=dict(
        model=model,
        tools=tools_list,
    ),
    user_agent_kwargs=dict(
        model=model,
    ),
    task_prompt=task_prompt,
    with_task_specify=False,
    output_language='中文'
)

# 设置聊天轮次限制
chat_turn_limit=5

print(
    Fore.GREEN
    + f"AI助手系统消息:\n{role_play_session.assistant_sys_msg}\n"
)
print(
    Fore.BLUE + f"AI用户系统消息:\n{role_play_session.user_sys_msg}\n"
)

print(Fore.YELLOW + f"原始任务提示:\n{task_prompt}\n")
print(
    Fore.CYAN
    + "指定的任务提示:"
    + f"\n{role_play_session.specified_task_prompt}\n"
)
print(Fore.RED + f"最终任务提示:\n{role_play_session.task_prompt}\n")

n = 0
input_msg = role_play_session.init_chat()
while n < chat_turn_limit:
    n += 1
    assistant_response, user_response = role_play_session.step(input_msg)

    if assistant_response.terminated:
        print(
            Fore.GREEN
            + (
                "AI助手终止。原因: "
                f"{assistant_response.info['termination_reasons']}."
            )
        )
        break
    if user_response.terminated:
        print(
            Fore.GREEN
            + (
                "AI用户终止。"
                f"原因: {user_response.info['termination_reasons']}."
            )
        )
        break

    # 打印用户的输出
    print_text_animated(
        Fore.BLUE + f"AI用户:\n\n{user_response.msg.content}\n"
    )

    if "CAMEL_TASK_DONE" in user_response.msg.content:
        break

    # 打印助手的输出，包括任何函数执行信息
    print_text_animated(Fore.GREEN + "AI助手:")
    tool_calls: list = assistant_response.info[
        'tool_calls'
    ]
    for func_record in tool_calls:
        print_text_animated(f"{func_record}")
    print_text_animated(f"{assistant_response.msg.content}\n")

    input_msg = assistant_response.msg

