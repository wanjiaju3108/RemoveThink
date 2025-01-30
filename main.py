from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类


"""
收到消息时，移除消息中的<think>标签及其内容
"""


# 注册插件
@register(name="RemoveThink", description="移除消息中的think标签及其内容", version="0.1", author="the-lazy-me")
class RemoveThinkPlugin(BasePlugin):

    # 插件加载时触发
    def __init__(self, host: APIHost):
        pass

    # 异步初始化
    async def initialize(self):
        pass

    def remove_think_content(self, msg: str) -> str:
        """移除消息中的think标签及其内容"""
        import re
        # 使用正则表达式匹配<think>标签及其内容
        pattern = r'<think>[\s\S]*?</think>'
        # 替换所有匹配项为空字符串
        result = re.sub(pattern, '', msg)
        # 去除首尾空白字符
        return result.strip()

    # 当收到回复消息时触发
    @handler(NormalMessageResponded)
    async def normal_message_responded(self, ctx: EventContext):
        msg = ctx.event.response_text
        if "<think>" in msg:
            # 处理消息
            processed_msg = self.remove_think_content(msg)
            ctx.add_return("reply", [processed_msg])

    # 插件卸载时触发
    def __del__(self):
        pass
