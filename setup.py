#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="nonebot_plugin_charpic",
    version="0.0.4",
    keywords=["pip", "nonebot_plugin_charpic"],
    description="Generate picture(or GIF) by character",
    long_description="Generate picture(or GIF) by character, for nonebot2 beta1",
    license="MIT Licence",
    url="https://github.com/RafuiiChan/nonebot_plugin_charpic",
    author="Yuyu1628", 
    author_email="a1628420979@163.com",
    packages=find_packages(include=["nonebot_plugin_charpic", "nonebot_plugin_charpic.*"]),
    include_package_data=True,
    platforms="any",
    install_requires=[
        "pillow >= 8.4.0",
        "aiohttp",
        "imageio >= 2.9.0",
        "nonebot2 >= 2.0.0rc1",
        "nonebot-adapter-onebot >= 2.0.0b1",
    ],
)
