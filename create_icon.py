#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
创建一个简单的图标文件
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size=256, output_file="icon.ico"):
    """创建一个简单的图标文件"""
    # 创建一个新的图像
    img = Image.new('RGBA', (size, size), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # 绘制一个圆形背景
    margin = int(size * 0.1)
    draw.ellipse([(margin, margin), (size - margin, size - margin)], fill=(0, 128, 0, 255))

    # 绘制文字
    try:
        font = ImageFont.truetype("arial.ttf", int(size * 0.5))
    except IOError:
        font = ImageFont.load_default()

    text = "SDP"
    # 在较新版本的PIL中，textsize已被弃用，改用font.getbbox或font.getsize
    try:
        text_width, text_height = font.getsize(text)
    except AttributeError:
        # 对于更新的Pillow版本
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

    position = ((size - text_width) // 2, (size - text_height) // 2)
    draw.text(position, text, font=font, fill=(255, 255, 255, 255))

    # 保存为ICO文件
    img.save(output_file, format='ICO', sizes=[(size, size)])

    print(f"图标已创建: {output_file}")

if __name__ == "__main__":
    create_icon()
