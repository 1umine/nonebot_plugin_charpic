import io
import ssl
import imageio
import httpx

from typing import List
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from nonebot.log import logger

default_font, font_size = Path(__file__).parent / "font" / "consola.ttf", 14
default_font = str(default_font)
util_draw = ImageDraw.Draw(Image.new("L", (1, 1)))

ssl_context = ssl.create_default_context()
ssl_context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_3
ssl_context.set_ciphers("HIGH:!aNULL:!MD5")
ntqq_img_client = httpx.AsyncClient(verify=ssl_context)


async def get_pic_text(_img: Image.Image, new_w: int = 150):
    str_map = "@@$$&B88QMMGW##EE93SPPDOOU**==()+^,\"--''.  "
    n = len(str_map)
    img = _img.convert("L")
    w, h = img.size
    if w > new_w:
        img = img.resize((new_w, int(new_w // 2 * h / w)))
    else:
        img = img.resize((w, h // 2))

    s = ""
    for x in range(img.height):
        for y in range(img.width):
            gray_v = img.getpixel((y, x))
            s += str_map[int(n * (gray_v / 256))]  # type: ignore
        s += "\n"
    return s


async def text_wh(
    font_filename, default_font_size: int, text: str
) -> tuple[ImageFont.FreeTypeFont, int, int]:
    """
    获取一段文本所占的宽度像素值
    返回字符画的 width, height
    """
    ttfont = ImageFont.truetype(font_filename, default_font_size)
    try:
        w, h = ttfont.getsize_multiline(text.strip())  # type: ignore
        return ttfont, w, h
    except AttributeError:  # PIL >= 10.0
        bbox: tuple[int, int, int, int] = util_draw.multiline_textbbox((0, 0), text, font=ttfont)  # type: ignore
        return ttfont, bbox[2], bbox[3]


async def text2img(text: str):
    font, w, h = await text_wh(default_font, font_size, text)
    img = Image.new("L", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text, fill="#000000", font=font)
    return img


async def char_gif(gif: Image.Image):
    """
    合成 gif 字符画
    """
    frame_list: List[Image.Image] = []
    try:
        while True:
            t = gif.tell()
            frame = await text2img(await get_pic_text(gif, new_w=80))
            frame_list.append(frame)
            gif.seek(t + 1)
    except EOFError:
        pass
    output = io.BytesIO()
    imageio.mimsave(output, frame_list, format="gif", duration=0.08)  # type: ignore
    return output


async def char_pic(img: Image.Image):
    if not img:
        return
    text = await get_pic_text(img)
    img = await text2img(text)
    output = io.BytesIO()
    img.save(output, format="jpeg")
    return output


async def get_img(img_url: str):
    if not img_url:
        return

    result = await ntqq_img_client.get(img_url)
    if result.status_code != 200:
        logger.warning(f"图片 {img_url} 下载失败: {result.status_code}")
        return None
    img = Image.open(io.BytesIO(result.content))
    return img
