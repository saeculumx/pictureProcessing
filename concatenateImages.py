import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib
import matplotlib.pyplot as plt
from pathlib import Path

matplotlib.use('TkAgg')


def words_to_picture(font, word):
    """
    Make words into picture
    :param font: font
    :param word: String word
    :return: Picture
    """
    word = word
    fontname = font.split(".")[-2]

    for w in word:
        print(w, fontname)
        if w == " ":
            a = np.ones([50, 30, 1]) * 255
            cv2.imwrite("blank.png", a)
