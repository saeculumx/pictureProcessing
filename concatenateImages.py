import string

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib
import matplotlib.pyplot as plt
from pathlib import Path

matplotlib.use('TkAgg')


def words_to_picture(font, word, font_colour, bkg_src, size_limit):
    """
    Make words into picture, fully auto
    :param size_limit: Size limit for the picture
    :param bkg_src:  background src for pic
    :param font_colour: font colour
    :param font: font
    :param word: String word
    :return: Picture which stacked together
    :return: Change Colour pictures
    """
    full_punc = 0
    blank_area_t = 0
    blank_area_b = 0
    word = word
    fontname = font.split(".")[-2]
    word_capital_array = []
    word_low_array = []
    word_array = []
    picture_array = []
    width_array = []
    stack = np.ones([128, 70, 3]) * 255
    for w in word:
        print(w, fontname)
        word_array.append(w)
        if w == " ":
            a = np.ones([128, 32, 3]) * 255
            cv2.imwrite("blank.png", a)
            picture_array.append(a)
        elif w.isupper():
            word_capital_array.append(w)
            upper_img = cv2.imread("final/{}".format(fontname + "/capital/" + w + "_" + fontname + ".png"))
            picture_array.append(upper_img)
        elif w in string.punctuation:
            word_capital_array.append(w)
            punc_img = cv2.imread("final/{}".format("punc" + "/capital/" + str(ord(w)) + "_" + "punc" + ".png"))
            picture_array.append(punc_img)
        else:
            word_low_array.append(w)
            low_img = cv2.imread("final/{}".format(fontname + "/low/" + w + "_" + fontname + ".png"))
            picture_array.append(low_img)

    i = 0
    for pic in picture_array:
        width = pic.shape[1]
        height = pic.shape[0]
        width_array.append(width)
        if height >= 128:
            height_loss = 0
            blank_area_t = np.ones([128 - height - height_loss, width, 3]) * 255
            blank_area_b = np.ones([height_loss, width, 3]) * 255
        elif word[i] == "p" or word[i] == "q" or word[i] == "g":
            o_img = cv2.imread("final/{}".format(fontname + "/low/" + "o" + "_" + fontname + ".png"))
            margin = 128 - o_img.shape[0] - 25
            height_loss = 128 - margin - o_img.shape[0]
            # print(margin)
            # print(height_loss)
            # print(margin + height_loss)
            blank_area_t = np.ones([margin, width, 3]) * 255
            blank_area_b = np.ones([128 - height - margin, width, 3]) * 255
        elif word[i] in string.punctuation:
            if width < 32:
                margin_l = round(32 - width / 2)
                margin_r = 32 - margin_l
                blank_area_l = np.ones([height, margin_l, 3]) * 255
                blank_area_r = np.ones([height, margin_r, 3]) * 255
                pic = np.hstack((blank_area_l, pic, blank_area_r))
                height = pic.shape[0]
                width = pic.shape[1]
                height_loss = 15
                blank_area_t = np.ones([128 - height - height_loss, width, 3]) * 255
                blank_area_b = np.ones([height_loss, width, 3]) * 255
            elif height < 110:
                height_loss = 15
                blank_area_t = np.ones([128 - height - height_loss, width, 3]) * 255
                blank_area_b = np.ones([height_loss, width, 3]) * 255
            else:
                height_loss = 0
                blank_area_t = np.ones([128 - height - height_loss, width, 3]) * 255
                blank_area_b = np.ones([height_loss, width, 3]) * 255
        else:
            height_loss = 25
            blank_area_t = np.ones([128 - height - height_loss, width, 3]) * 255
            blank_area_b = np.ones([height_loss, width, 3]) * 255
        # print("T/P/B: " + word[i] + " | " + str(blank_area_t.shape[0]) + " | " + str(height) + " | " + str(
        #     blank_area_b.shape[0]))
        full = np.vstack((blank_area_t, pic, blank_area_b))
        # print("Full: " + str(full.shape))
        pre_stack = np.hstack((stack, full))
        if pre_stack.shape[1]>size_limit:
            print("Exceeds")
            # stack = np.hstack((stack, full))
            remaining_array = np.array_split(np.array(picture_array),i,axis=0)
            print(len(remaining_array))
            break
        else:
            stack = np.hstack((stack, full))
        i = i + 1

    change_colour = Image.fromarray(stack.astype('uint8'), 'RGB')
    width, height = change_colour.size
    bkg_src_p = Image.open(bkg_src)
    for w in range(width):
        for h in range(height):
            current_color = change_colour.getpixel((w, h))
            if current_color == (255, 255, 255):
                # change_colour.putpixel((w, h), bkg_colour)
                b_current_color = bkg_src_p.getpixel((w, h))
                change_colour.putpixel((w, h), b_current_color)
                # print("CUR: BACK")
            elif current_color == (0, 0, 0):
                # print("CUR: FONT")
                change_colour.putpixel((w, h), font_colour)
    cv2.imshow('image', stack)
    cv2.waitKey(0)
    return stack, change_colour
