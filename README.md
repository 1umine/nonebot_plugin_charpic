<div align="center">

# 生成字符画（或GIF）

</div>

<p align="center">
  
  <a href="https://github.com/1umine/nonebot_plugin_charpic/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-informational">
  </a>
  <a href="https://github.com/nonebot/nonebot2">
    <img src="https://img.shields.io/badge/nonebot2-red">
  </a>
  
</p>
</p>

## 安装

1. 通过`pip`或`nb`安装；

命令

1. 使用 nb-cli , 需要在 bot 根目录下执行
```
nb plugin install nonebot_plugin_charpic
```

2. 使用 pip ，安装完需要手动在 pyproject.toml 中的 `tool.nonebot.plugins` 中添加 `nonebot_plugin_charpic` 以加载插件
```
pip install nonebot_plugin_charpic
```

## 功能

合成字符画(或 gif )

## 使用方法

`字符画` + `图片`，图片支持从回复消息中获取

⚠ 需要 nonebot2 配置的命令前缀，如果没配置默认 `/` 

## 可能遇到的问题

### 缺资源
（没有字体的话可以尝试以下解决方案）
1. 找到这个包(一般在`site-packages`目录下)，将`data_source.py`中的`Path(__file__).parent / "font" / "consola.ttf"`改为你自己想要的字体的路径；
2. 在`__init__.py`同级目录创建文件夹，名为 `font`, 再下载本仓库中的字体放进去。
3. 直接clone本仓库，安装好依赖，放在bot能导入到的文件夹下面 ~~（dddd）~~
