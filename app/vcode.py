# -*- coding: utf8 -*-

import hashlib
from io import BytesIO
import random
import datetime
import base64

from PIL import Image, ImageDraw, ImageFont

def gen_rand_str():
    '''生成4位随机字符'''

    mp = hashlib.md5()
    mp.update(str(datetime.datetime.now()).encode()+str(random.random()).encode())   
    return mp.hexdigest()[:4]

def make_image(FONT, s):
    '''创建验证码图片和字符'''

    font = ImageFont.truetype(FONT, 22)
    width = 75
    height = 35 

    #图像大小、颜色
    img = Image.new('RGB', (width, height), '#088A85')

    draw = ImageDraw.Draw(img)

    #干扰线
    for x in range(5):
        draw.line((
            random.randint(0, width), 
            random.randint(0, height), 
            random.randint(0, width), 
            random.randint(0, height)
        ))

    #字符
    draw.text((15, 4), s, font=font)   
    del draw   

    buffer = BytesIO()
    img.save(buffer, 'jpeg')
    
    return buffer
