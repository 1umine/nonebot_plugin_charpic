from nonebot import on_command, require
from nonebot.typing import T_State
from nonebot.adapters import Message
from nonebot.plugin import PluginMetadata, inherit_supported_adapters

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import Image, UniMessage

from .data_source import char_gif, get_img, char_pic
from .depends import Images


__plugin_meta__ = PluginMetadata(
    name="charpic",
    description="合成字符画",
    usage="/字符画 <图片>",
    type="application",
    homepage="https://github.com/1umine/nonebot_plugin_charpic",
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
)

pic2text = on_command("字符画", priority=50, block=True)


@pic2text.handle()
async def _(state: T_State, images: list[Image] = Images()):
    if images:
        state["image"] = images


@pic2text.got("image", prompt="图呢？")
async def generate_(state: T_State):
    msg: list[Image] | Message = state["image"]
    img_urls: list[str] = []
    if isinstance(msg, Message):
        imgs: list[Image] = UniMessage.generate_without_reply(message=msg).get(Image) # type: ignore
        img_urls = [i.url for i in imgs if i.url]
    else:
        img_urls = [i.url for i in msg if i.url]
    if not img_urls:
        await pic2text.finish("未获取到任何图片")

    await pic2text.send("努力生成中...")
    pic = await get_img(img_urls[0])  # 取图
    if not pic:
        await pic2text.finish(message="图片未获取到，请稍后再试")

    if pic.format == "GIF":
        res = await char_gif(pic)
        await UniMessage.image(raw=res).send()
    else:
        res = await char_pic(pic)
        await UniMessage.image(raw=res).send()
