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
        super().__init__(host)  # 必须调用父类的初始化方法

    # 异步初始化
    async def initialize(self):
        pass

    def remove_think_content(self, msg: str) -> str:
        """移除消息中的think标签及其内容"""
        import re
        # 使用正则表达式匹配<think>标签及其内容
        pattern = r'<think>[\s\S]*?</think>'
        
        result = msg
        iteration = 0
        max_iterations = 10  # 设置最大迭代次数，防止无限循环
        
        while "<think>" in result and iteration < max_iterations:
            # 输出调试信息
            think_blocks = re.findall(pattern, result)
            print(f"第{iteration + 1}次处理，找到 {len(think_blocks)} 个think标签块")
            for i, block in enumerate(think_blocks):
                print(f"第{i+1}个think块: {block[:100]}...")
            
            # 替换所有匹配项为空字符串
            result = re.sub(pattern, '', result)
            # 去除首尾空白字符和多余的空行
            result = re.sub(r'\n\s*\n', '\n', result.strip())
            
            iteration += 1
        
        if iteration >= max_iterations:
            print(f"警告：达到最大迭代次数 {max_iterations}，可能存在异常标签")
            
        print(f"处理后的消息: {result}")
        return result

    # 当收到回复消息时触发
    @handler(NormalMessageResponded)
    async def normal_message_responded(self, ctx: EventContext):
        msg = ctx.event.response_text
        if "<think>" in msg:
            # 处理消息
            processed_msg = self.remove_think_content(msg)
            # 如果处理后的消息为空，不进行回复
            if processed_msg:
                ctx.add_return("reply", [processed_msg])
            else:
                self.ap.logger.warning("处理后的消息为空，跳过回复")

    # 插件卸载时触发
    def __del__(self):
        pass
