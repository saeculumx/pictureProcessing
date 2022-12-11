import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib
import matplotlib.pyplot as plt
from pathlib import Path

matplotlib.use('TkAgg')


def generate_pics(height, width, text, font, f_size, capital, form=None):
    """
    This Function generate pictures with english letters
    :param form: format either punc/number
    :param capital: if the word is capital
    :param height: height of the picture
    :param width: width of the picture
    :param text: text of the picture
    :param font: font of the picture
    :param f_size: size of the picture
    :return: a picture with a text
    """
    f_size = f_size

    if form == "punc":
        text_font = ImageFont.truetype("arial.ttf", size=f_size)
        text_chr = chr(int(text))
        base_img = Image.new('RGB', (width, height), color='White')
        draw_img = ImageDraw.Draw(base_img)
        text_width, text_height = draw_img.textsize(text_chr, font=text_font)
        x_text = (width - text_width) / 2
        y_text = (height - text_height) / 2
        draw_img.text((x_text, y_text), text_chr, font=text_font, fill=(0, 0, 0))
        Path("generate/{}".format(font + "_" + capital)).mkdir(parents=True, exist_ok=True)
        fontname = "punc"
        print(">>GEN<< File generated at : generate/" + font + capital + "/{}.png".format(text + "_" + fontname))
        base_img.save("generate/" + font + "_" + capital + "/{}.png".format(text + "_" + fontname))
    else:
        text_font = ImageFont.truetype(font, size=f_size)
        text = text
        base_img = Image.new('RGB', (width, height), color='White')
        draw_img = ImageDraw.Draw(base_img)
        text_width, text_height = draw_img.textsize(text, font=text_font)
        x_text = (width - text_width) / 2
        y_text = (height - text_height) / 2
        draw_img.text((x_text, y_text), text, font=text_font, fill=(0, 0, 0))
        Path("generate/{}".format(font + "_" + capital)).mkdir(parents=True, exist_ok=True)
        print(font)
        fontname = font.split(".")[-2]
        print(">>GEN<< File generated at : generate/" + font + "_" + capital + "/{}.png".format(text + "_" + fontname))
        base_img.save("generate/" + font + "_" + capital + "/{}.png".format(text + "_" + fontname))
