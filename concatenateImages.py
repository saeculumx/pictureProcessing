import string

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib
import matplotlib.pyplot as plt
from pathlib import Path
from sympy import symbols, solve
from numpy import ceil

matplotlib.use('TkAgg')


def words_to_picture(font, word, font_colour, bkg_src, size_limit, padding, filename=None):
    """
    Make words into picture, fully auto
    :param filename: Filename for massive production
    :param padding: TBLR
    :param size_limit: Size limit for the picture
    :param bkg_src:  background src for pic
    :param font_colour: font colour
    :param font: font
    :param word: String word
    :return: Picture which stacked together
    :return: Change Colour pictures
    """

    word = word
    fontname = font.split(".")[-2]
    word_capital_array = []
    word_low_array = []
    word_array = []
    picture_array = []
    width_array = []
    number_array = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    def split_word(word_str):
        #print(">>CON<< Word: ", word_str, " | ", fontname, " | ", len(word_str))
        for w in word_str:
            word_array.append(w)
            if w == " ":
                a = np.ones([128, 32, 3]) * 255
                cv2.imwrite("blank.png", a)
                picture_array.append(a)
            elif w.isupper():
                # print("Upper ", "final/{}".format(fontname + "/capital/" + w + "_" + fontname + ".png"))
                word_capital_array.append(w)
                upper_img = cv2.imread("final/{}".format(fontname + "/capital/" + w + "_" + fontname + ".png"))
                picture_array.append(upper_img)
            elif w in string.punctuation:
                # print("Punc ", "final/{}".format("punc" + "/capital/" + str(ord(w)) + "_" + "punc" + ".png"))
                word_capital_array.append(w)
                punc_img = cv2.imread("final/{}".format("punc" + "/capital/" + str(ord(w)) + "_" + "punc" + ".png"))
                picture_array.append(punc_img)
            elif w in number_array:
                # print("Numbers ", "final/{}".format(fontname + "/capital/" + w + "_" + fontname + ".png"))
                word_capital_array.append(w)
                upper_img = cv2.imread("final/{}".format(fontname + "/capital/" + w + "_" + fontname + ".png"))
                picture_array.append(upper_img)
            else:
                # print("Others ", "final/{}".format(fontname + "/low/" + w + "_" + fontname + ".png"))
                word_low_array.append(w)
                low_img = cv2.imread("final/{}".format(fontname + "/low/" + w + "_" + fontname + ".png"))
                picture_array.append(low_img)

    split_word(word)

    def pic_process(array, txt_array):
        global after_stack
        after_stack = np.ones([128, 0, 3]) * 255
        stack = np.ones([128, 0, 3]) * 255
        i = 0
        # stack = np.ones([128, 0, 3]) * 255
        for pic in array:
            if pic is None:
                print(txt_array[i])
            width = pic.shape[1]
            height = pic.shape[0]
            width_array.append(width)
            if height >= 120:
                height_loss = 0
                blank_area_t = np.ones([128 - height - height_loss, width, 3]) * 255
                blank_area_b = np.ones([height_loss, width, 3]) * 255
            elif txt_array[i] == "p" or txt_array[i] == "q" or txt_array[i] == "g" or txt_array[i] == "y":
                o_img = cv2.imread("final/{}".format(fontname + "/low/" + "o" + "_" + fontname + ".png"))
                margin = 128 - o_img.shape[0] - 25
                blank_area_t = np.ones([margin, width, 3]) * 255
                blank_area_b = np.ones([128 - height - margin, width, 3]) * 255
            elif txt_array[i] in string.punctuation:
                if width < 32:
                    # margin_l = round(32 - width / 2)
                    # margin_r = 32 - margin_l
                    # blank_area_l = np.ones([height, margin_l, 3]) * 255
                    # blank_area_r = np.ones([height, margin_r, 3]) * 255
                    # pic = np.hstack((blank_area_l, pic, blank_area_r))
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
                if height + height_loss > 128:
                    height_loss = 128 - height
                blank_area_t = np.ones([128 - height - height_loss, width, 3]) * 255
                blank_area_b = np.ones([height_loss, width, 3]) * 255
            full = np.vstack((blank_area_t, pic, blank_area_b))
            stack = np.hstack((stack, full))
            # print("OG_Stack: ", stack.shape[1])
            i = i + 1
        return stack

    def v_page_stack(array, sep_wod_array):
        out_path = "txt"
        #out_path = "D:/py/Scene_Text_Spotting/dataset/my_data/label"
        i = 0
        full_array = []
        label_array = []
        txt_array = []
        full_pic = np.ones([padding[0], size_limit + padding[2] + padding[3], 3]) * 255
        full_pic_bot = np.ones([padding[1], size_limit + padding[2] + padding[3], 3]) * 255
        for ele in array:
            height = ele.shape[0]
            width = ele.shape[1]
            pad_left = np.ones([height, padding[2], 3]) * 255
            pad_right = np.ones([height, padding[3], 3]) * 255
            if not label_array:
                st = "{},{},{},{},{},{},{},{},{}".format(padding[0],padding[1]+20,
                                                         padding[0]+width,padding[1]+20,
                                                         padding[0]+width,padding[1]+height-35,
                                                         padding[0],padding[1]+height-35,sep_wod_array[0])
                # print("ST",st)
                txt_array.append(st)
                label_array.append([[padding[0],padding[1]],
                                    [padding[0]+width,padding[1]],
                                    [padding[0]+width,padding[1]+height],
                                    [padding[0],padding[1]+height], sep_wod_array[0]])
                i += 1
            else:
                lab = label_array[i - 1]
                st2 = "{},{},{},{},{},{},{},{},{}".format(lab[3][0],lab[3][1]+20,
                                                          lab[3][0]+width,lab[3][1]+20,
                                                          lab[3][0]+width,lab[3][1]-35 + height,
                                                          lab[3][0], lab[3][1]-35 + height,sep_wod_array[i])
                # print("ST2:",lab[3][0],",",lab[3][1],",",lab[2][0],",",lab[2][1],",",lab[2][0] + height, ",",width,",",0,",", lab[3][1] + height,",", sep_wod_array[i])
                label_array.append([lab[3],
                                    [lab[3][0]+width,lab[3][1]],
                                    [lab[3][0]+width,lab[3][1] + height],
                                    [lab[3][0], lab[3][1] + height], sep_wod_array[i]])
                txt_array.append(st2)
                i += 1
            if ele.shape[1] < size_limit:
                width_loss = size_limit - ele.shape[1]
                width_patch = np.ones([ele.shape[0], width_loss, 3]) * 255
                full = np.hstack((pad_left, ele, width_patch, pad_right))
                full_array.append(full)
            else:
                cropped = ele[0:ele.shape[0], 0:size_limit]
                #print(cropped.shape)
                cropped = np.hstack((pad_left, cropped, pad_right))
                full_array.append(cropped)
        for fs in full_array:
            full_pic = np.vstack((full_pic, fs))
        full_pic = np.vstack((full_pic, full_pic_bot))
        #("label:",label_array)
        Path("{}/{}".format(out_path,fontname)).mkdir(parents=True, exist_ok=True)
        if filename == "":
            open('{}/outcome.txt'.format(out_path), 'w').close()
            for lbu in txt_array:
                # lbu = str(lbu).replace('[', '').replace(']', '').replace('\'', '').replace('\"', '')
                # lbu = str(lbu).replace(" ", "")
                with open('{}/outcome.txt'.format(out_path), 'a') as f:
                    f.write(str(lbu))
                    f.write('\n')
            # cv2.imshow("full.png", full_pic)
            # cv2.waitKey(0)
            return full_pic
        else:
            open("{}/{}/".format(out_path,fontname) + "{}.txt".format(filename), 'w').close()
            for lbu in txt_array:
                # lbu = str(lbu).replace('[', '').replace(']', '').replace('\'', '').replace('\"', '')
                # lbu = str(lbu).replace(" ", "")
                with open("{}/{}/".format(out_path,fontname) + "{}.txt".format(filename), 'a') as f:
                    f.write(str(lbu))
                    f.write('\n')
            # cv2.imshow("full.png", full_pic)
            # cv2.waitKey(0)
            return full_pic

    # cv2.imshow('image', final_stack)
    # cv2.waitKey(0)
    def multi_init(stack):
        #print("size limit : ", size_limit)
        size_multiplier = ceil(stack.shape[1] / size_limit)
        indicators = []
        sum = 0
        fsum = 0
        i = 0
        for pic in picture_array:
            p_wid = pic.shape[1]
            if sum + p_wid > size_limit:
                indicators.append(i)
                sum -= sum
            sum += p_wid
            fsum += p_wid
            i += 1
        f = len(picture_array)
        z = len(indicators)
        i = 0
        sep_array = []
        sep_wod_array = []
        for ind in indicators:
            if i == 0:
                # print("sep_array: ", 0, ind)
                ind_arr = picture_array[0:ind]
                sp_word = word[0:ind]
                sep_array.append(ind_arr)
                sep_wod_array.append(sp_word)
                i += 1
            else:
                # print("sep_array: ", indicators[i - 1], ind)
                ind_arr = picture_array[indicators[i - 1]:ind]
                sp_word = word[indicators[i - 1]:ind]
                sep_array.append(ind_arr)
                sep_wod_array.append(sp_word)
                i += 1
        # print("sep_array: ", indicators[z - 1], f - 1)
        if z != 0:
            ind_arr = picture_array[indicators[z - 1]:f - 1]
            sep_array.append(ind_arr)
            sp_word = word[indicators[z - 1]:f - 1]
            sep_wod_array.append(sp_word)
        else:
            sep_array.append(picture_array)
            sep_wod_array.append(word)
        #print("len: sep_array: ", len(sep_array))
        #print("indicators: ", indicators)
        #print("stack_sum: ", fsum, stack.shape[1])
        #print("size_multiplier: ", size_multiplier)
        #print("words: ", sep_wod_array)

        final_pic_array = []
        i = 0
        for sep in sep_array:
            pic = pic_process(sep, sep_wod_array[i])
            # print("Shape: ", pic.shape[1])
            final_pic_array.append(pic)
            # cv2.imshow("pic", pic)
            # cv2.waitKey(0)
            i += 1
        return v_page_stack(final_pic_array, sep_wod_array)

    def apply_bkg(stack):
        out_path = "outcome"
        #out_path = "D:/py/Scene_Text_Spotting/dataset/my_data/image"
        if bkg_src != "":
            change_colour = Image.fromarray(stack.astype('uint8'), 'RGB')
            cg_width, cg_height = change_colour.size
            bkg_src_p = Image.open(bkg_src)
            for_process = cv2.imread(bkg_src)
            if bkg_src_p.width < cg_width or bkg_src_p.height < cg_height:
                dim = (cg_width, cg_height)
                for_process = cv2.resize(for_process, dim, interpolation=cv2.INTER_AREA)
                bkg_src_p = Image.fromarray(np.uint8(for_process))
                #print("Background picture is not big enough, required ", cg_width, cg_height)
            for wd in range(cg_width):
                for hd in range(cg_height):
                    current_color = change_colour.getpixel((wd, hd))
                    if current_color == (255, 255, 255):
                        b_current_color = bkg_src_p.getpixel((wd, hd))
                        change_colour.putpixel((wd, hd), b_current_color)
                    elif current_color == (0, 0, 0):
                        change_colour.putpixel((wd, hd), font_colour)
            colour = cv2.cvtColor(np.array(change_colour), cv2.COLOR_RGB2BGR)
            # cv2.imshow("pic", colour)
            # cv2.waitKey(0)
            Path(out_path).mkdir(parents=True, exist_ok=True)
            if filename != "":
                Path("{}/{}".format(out_path,fontname)).mkdir(parents=True, exist_ok=True)
                cv2.imwrite("{}/{}/".format(out_path,fontname) + "{}_b.png".format(filename), colour)
                return change_colour
            else:
                cv2.imshow("pic", colour)
                cv2.waitKey(0)
                return change_colour
        else:
            if filename != "":
                Path("{}/{}".format(out_path,fontname)).mkdir(parents=True, exist_ok=True)
                cv2.imwrite("{}/{}/".format(out_path,fontname) + "{}.png".format(filename), stack)
                return stack
            else:
                cv2.imshow("pic", stack)
                cv2.waitKey(0)
                return stack

    # v_page_array = []
    # v_page_array.append(apply_bkg(final_stack))
    # v_page_array.append(apply_bkg(after_stack))

    final_stack = pic_process(picture_array, word)
    com_stack = multi_init(final_stack)
    apply_bkg(com_stack)

    # v_page_stack(v_page_array)
    # pre_stack = np.hstack((stack, full))
    # if pre_stack.shape[1] > size_limit:
    #     print("Exceeds")
    #     size_multiplier = ceil(pre_stack.shape[1]/size_limit)
    #     print(size_multiplier)
    #     remaining_array = picture_array[i:len(picture_array) + 1]
    #     dup = word[0:i]
    #     text_array = word[i:len(picture_array) + 1]
    #     print(" | ", dup, " | ", text_array, " | ")
    #     after_stack = pic_process(remaining_array, text_array)
    #     # cv2.imshow('image', after_stack)
    #     # cv2.waitKey(0)
    #     break
    # else:
