import importlib
from base64 import b64encode
from typing import Dict
from io import BytesIO

from nonebot.adapters import Bot, MessageSegment
from nonebot.internal.matcher import current_bot
from nonebot.utils import is_coroutine_callable


async def ob12_img(data: bytes):
    """适配 Onebot V12 图片消息"""
    from nonebot.adapters.onebot.v12 import MessageSegment

    bot = current_bot.get()
    resp = await bot.upload_file(type="data", name=f"charpic-{hash(data)}", data=data)
    return MessageSegment.image(resp["file_id"])


def mirai2_img(data: bytes):
    from nonebot.adapters.mirai2 import MessageSegment as ms

    return ms.image(base64=f"base64://{b64encode(data).decode()}")


platform_img: Dict[str, list] = {
    "Telegram": ["File", "photo"],  # telegram.message.File.photo
    "QQ": ["file_image"],  # qq.message.MessageSegment.file_image
    "OneBot V12": [ob12_img],  # function `ob12_img`
    "mirai2": [mirai2_img],  # func `mirai2_img`
}
"""
适配器名称：图片构造方法路径

各平台图片消息段构造方法，通过在此定义图片消息段构造方法以适配不同平台图片消息

说明：
    列表内元素可为函数对象，应支持 bytes 入参，1 个元素


    列表内元素为字符串，表示对应适配器图片构造方法

        元素个数为 1 时，消息段类名默认 MessageSegment

        否则第一个元素为消息段类名，第二个为图片消息段构造方法

    不在列表中的适配器直接返回 {adapter}.message.MessageSegment.image 

"""


class AdapterNotFound(Exception):
    pass


def get_seg_constructor(mod, path: list = None):
    """获取图片消息段构造方法，需支持 `bytes` 入参"""
    if not path:
        return mod.MessageSegment.image
    if len(path) == 1 and isinstance(path[0], str):
        path.insert(0, "MessageSegment")
    r = None
    for p in path:
        if isinstance(p, str):
            r = getattr(mod, p)
        else:
            return p
    return r


async def Image(file: BytesIO, bot: Bot) -> MessageSegment:
    adapter_module = bot.adapter.__class__.__module__.rstrip(".adapter")
    adapter_name = bot.adapter.get_name()
    try:
        mod = importlib.import_module(f"{adapter_module}.message")
        try:
            image_constructor = get_seg_constructor(mod, platform_img.get(adapter_name))
        except AttributeError:
            raise AttributeError("平台可能不支持图片消息")
        if is_coroutine_callable(image_constructor):
            return await image_constructor(file.getvalue())
        return image_constructor(file.getvalue())
    except ModuleNotFoundError:
        raise AdapterNotFound(f"适配器 {adapter_name} 不存在，请检查适配器是否安装")
