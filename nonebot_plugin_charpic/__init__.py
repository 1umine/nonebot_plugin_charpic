from typing import List, Type
from nonebot import on_command
from nonebot.adapters import Bot, Message, MessageSegment
from nonebot.typing import T_State
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata

from .data_source import get_img, char_gif, get_pic_text, text2img
from .adapter import Image


__plugin_meta__ = PluginMetadata(
    name="charpic",
    description="合成字符画",
    usage="/字符画 <图片>",
    type="application",
    homepage="https://github.com/1umine/nonebot_plugin_charpic",
    supported_adapters={
        "~onebot.v11",
        "~onebot.v12",
        "~qq",
        "~mirai2",
    },
)

pic2text = on_command("字符画", priority=26, block=True)


@pic2text.handle()
async def _(state: T_State, args: Message = CommandArg()):
    for seg in args:
        if seg.type == "image":
            state["image"] = [seg]


@pic2text.got("image", prompt="图呢？")
async def generate_(bot: Bot, state: T_State):
    msg: List[Type[MessageSegment]] = state["image"]
    if msg[0].type == "image":
        url: str = msg[0].data.get("url") or await pic2text.finish(
            "无法获取图片链接"
        )  # 获取图片链接，需要有 url 字段（别的感觉太麻烦，摆了）
        await pic2text.send("努力生成中...")

        pic = await get_img(url)  # 取图
        if not pic:
            await pic2text.finish(message="图片未获取到，请稍后再试")

        if pic.format == "GIF":
            res = await char_gif(pic)
            await pic2text.finish(await Image(res, bot))
        text = await get_pic_text(pic)
        if text:
            res = await text2img(text)
            await pic2text.finish(await Image(res, bot))
    else:
        await pic2text.finish("没有发现图片")
