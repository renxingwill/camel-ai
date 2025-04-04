from PIL import Image
from io import BytesIO
import requests
from camel.messages import BaseMessage
from camel.types import RoleType
# 下载一张图片并创建一个 PIL Image 对象
url = "https://raw.githubusercontent.com/camel-ai/camel/master/misc/logo_light.png"
response = requests.get(url)
img = Image.open(BytesIO(response.content))

# 创建包含图片的用户消息
image_message = BaseMessage(
    role_name="User_with_image",
    role_type=RoleType.USER,
    content="Here is an image",
    meta_dict={},
    image_list=[img]  # 将图片列表作为参数传入
)
from camel.messages import BaseMessage

# 创建用户消息
user_msg = BaseMessage.make_user_message(
    role_name="User_1",
    content="Hi, what can you do?"
)

# 创建助手消息
assistant_msg = BaseMessage.make_assistant_message(
    role_name="Assistant_1",
    content="I can help you with various tasks."
)

print("User Message:", user_msg)
print("Assistant Message:", assistant_msg)
print(image_message)
msg_dict = image_message.to_dict()
print("Message as dict:", msg_dict)
from camel.types import OpenAIBackendRole

# 将用户消息转化为OpenAI后端兼容的用户消息
openai_user_msg = user_msg.to_openai_message(role_at_backend=OpenAIBackendRole.USER)
print("OpenAI-compatible user message:", openai_user_msg)

# 将助手消息转化为OpenAI后端的助手消息
openai_assistant_msg = assistant_msg.to_openai_assistant_message()
print("OpenAI-compatible assistant message:", openai_assistant_msg)
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.models import ModelFactory
from camel.types import ModelPlatformType,RoleType

from io import BytesIO
import requests
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('QWEN_API_KEY')

model = ModelFactory.create(
    model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
    model_type="Qwen/QVQ-72B-Preview",
    url='https://api-inference.modelscope.cn/v1/',
    api_key=api_key
)

# 实例化ChatAgent
chat_agent = ChatAgent(model=model,output_language='中文')

# 图片URL
url = "https://img0.baidu.com/it/u=2205376118,3235587920&fm=253&fmt=auto&app=120&f=JPEG?w=846&h=800"
response = requests.get(url)
img = Image.open(BytesIO(response.content))

user_image_msg = BaseMessage.make_user_message(
    role_name="User", 
    content="请描述这张图片的内容", 
    image_list=[img]  # 将图片放入列表中
)

# 将包含图片的消息传给ChatAgent
response_with_image = chat_agent.step(user_image_msg)
print("Assistant's description of the image:", response_with_image.msgs[0].content)
from camel.responses import ChatAgentResponse
from camel.messages import BaseMessage
from camel.types import RoleType

# 创建一个 ChatAgentResponse 实例
response = ChatAgentResponse(
    msgs=[
        BaseMessage(
            role_name="Assistant",  # 助手的角色名称
            role_type=RoleType.ASSISTANT,  # 指定角色类型
            content="你好，我可以帮您做什么？",  # 消息内容
            meta_dict={}  # 提供一个空的元数据字典（可根据需要填充）
        )
    ],  
    terminated=False,  # 会话未终止
    info={"usage": {"prompt_tokens": 10, "completion_tokens": 15}}  # 附加信息
)

# 访问属性
messages = response.msgs  # 获取Agent生成的消息
is_terminated = response.terminated  # 会话是否终止
additional_info = response.info  # 获取附加信息

# 打印消息内容
print("消息内容:", messages[0].content)
# 打印会话是否终止
print("会话是否终止:", is_terminated)
# 打印附加信息
print("附加信息:", additional_info)
