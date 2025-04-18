from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import aiohttp

from astrbot.core import AstrBotConfig


@register("linregai", "小新", "一个天堂辅助充值插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config
        # print(self.config)

    async def send_data(self, token, url, payload):
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            async with session.post(url, headers=headers, json=payload) as response:
                return await response.text()

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/lin` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("lin", alias={'充值', '天堂'})
    async def lin(self, event: AstrMessageEvent):
        """这是一个 hello world 指令"""  # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        user_name = event.get_sender_name()
        message_str = event.message_str  # 用户发的纯文本消息字符串
        message_chain = event.get_messages()  # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        workflow_id = self.config.get("workflow_id")
        token = self.config.get("token")
        # print(f"{token} - {workflow_id}")
        json = {
            "workflow_id": workflow_id,
            "parameters": {
                "input": message_str
            }
        }
        response = await self.send_data(token, "https://api.coze.cn/v1/workflow/run", json)
        logger.info(message_chain)
        yield event.plain_result(f"你好，{user_name}, 你发了 {message_str}! 智能体处理结果：{response}")  # 发送一条纯文本消息

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
