<div align="center">

# 生成字符画（包括GIF）

</div>

<p align="center">
  
  <a href="https://github.com/RafuiiChan/nonebot_plugin_charpic/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-informational">
  </a>
  
  <a href="https://github.com/nonebot/nonebot2">
    <img src="https://img.shields.io/badge/nonebot2-2.0.0rc1-green">
  </a>
  
  <a href="">
    <img src="https://img.shields.io/badge/release-v0.0.3-orange">
  </a>
  
</p>
</p>

## 版本

v0.0.4

⚠ 适配nonebot2-2.0.0rc1；

## 安装

1. 通过`pip`或`nb`安装；

命令

`nb plugin install nonebot_plugin_charpic`

`pip install nonebot_plugin_charpic`

## 功能

合成字符画(或 gif )

## 命令

`字符画` + `图片`

⚠ 需要 nonebot2 配置的命令前缀，如果没配置默认 `/`  ~~（好像是吧）~~

## 问题


### 缺资源
（纯萌新，第一次发包，不太熟，没有字体的话可以尝试以下解决方案）
1. 找到这个包(一般在`site-packages`目录下)，将`data_source.py`中的`Path(__file__).parent / "font" / "consola.ttf"`改为你自己想要的字体的路径；
2. 在`__init__.py`同级目录创建文件夹，名为 `font`, 再下载本仓库中的字体放进去。
3. 直接clone本仓库，安装好依赖，放在bot能导入到的文件夹下面 ~~（dddd）~~
