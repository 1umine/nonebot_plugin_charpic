from nonebot.adapters import Bot, Event
from nonebot.params import Depends
from nonebot_plugin_alconna.uniseg import reply_fetch
from nonebot_plugin_alconna import UniMessage, Image


async def get_images(bot: Bot, event: Event):
    reply = await reply_fetch(event, bot)
    msg = UniMessage.generate_without_reply(event=event, bot=bot)
    if reply:
        msg.extend(UniMessage.generate_without_reply(message=reply.msg))  # type: ignore
    return msg.get(Image)


def Images():
    """
    消息包含的图片

    支持获取回复的消息中的图片
    """
    return Depends(get_images)
