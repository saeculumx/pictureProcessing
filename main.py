import random
import string

import concatenateImages
import fileGenerator
import importPics
from string import ascii_lowercase as alc
from string import ascii_uppercase as ulc

if __name__ == '__main__':
    font_arrays = ["arial.ttf", "BAUHS93.TTF", "calibri.ttf", "comic.ttf", "cour.ttf", "NIAGENG.TTF", "JOKERMAN.TTF",
                   "FRSCRIPT.TTF", "BRLNSR.TTF", "BOD_CBI.TTF"]
    filetype = ".png"
    font = font_arrays[9]
    font_colour = (255, 255, 255)
    bkg_colour = (42, 56, 67)
    padding = [50, 50, 50, 50]  # top,bottom,left,right
    number_array = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


    def generate_cut():
        for punc in string.punctuation:
            text = str(ord(punc))
            fontname = "punc"
            print(">>GEN<< : Punc is : {} || ".format(ord(punc)) + punc)
            src_fontname = "punc"
            filename = text + "_" + src_fontname + filetype
            # print(filename)
            fileGenerator.generate_pics(128, 128, text, fontname, 90, capital="capital", form=fontname)
            importPics.img_bw("generate/{}".format("punc" + "_capital" + "/" + filename), capital="capital")

        for number in number_array:
            text = str(number)
            fontname = font.split(".")[-2]
            print(">>GEN<< : Number is : {} || ".format(text), fontname)
            filename = text + "_" + fontname + filetype
            fileGenerator.generate_pics(128, 128, text, font, 90, capital="capital", form="number")
            importPics.img_bw("generate/{}".format(font + "_capital" + "/" + filename), capital="capital")

        for i in ulc:
            text = i
            fontname = font.split(".")[-2]
            filename = text + "_" + fontname + filetype
            fileGenerator.generate_pics(128, 128, text, font, 90, capital="capital")
            importPics.img_bw("generate/{}".format(font + "_capital" + "/" + filename), capital="capital")

        for i in alc:
            text = i
            fontname = font.split(".")[-2]
            filename = text + "_" + fontname + filetype
            fileGenerator.generate_pics(128, 128, text, font, 90, capital="low")
            importPics.img_bw("generate/{}".format(font + "_low" + "/" + filename), capital="low")


    def rd_string_generator(length):
        selections = [0, 1, 2]
        letters = string.ascii_letters
        numbers = string.digits
        punc_ls = [" "]
        punc = [44, 46, 33, 63, 37, 40, 41, 91, 93, 123, 125, 60, 62, 126, 43, 45, 61, 39, 34, 58, 59]
        for p in punc:
            punc_ls.append(chr(p))
        super_array = []
        for le in letters:
            super_array.append(le)
        for nu in numbers:
            super_array.append(nu)
        for pu in punc_ls:
            super_array.append(pu)
        # print(super_array)
        rand = "".join(random.choices(super_array, k=length))
        return rand

    def init_automatic():
        for fo in font_arrays:
            i = 1
            while i < 10:
                stt = rd_string_generator(10)
                # print(stt)
                concatenateImages.words_to_picture(fo, stt, font_colour, "bkg.png",
                                                   1200, padding, i)
                concatenateImages.words_to_picture(fo, stt, font_colour, "",
                                                   1200, padding, i)
                i += 1


    # generate_cut()
    Li = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam. sunt in culpa qui officia deserunt mollit anim id est laborum."
    # init_automatic()
    concatenateImages.words_to_picture(font_arrays[0], Li, font_colour, "",
                                       1200, padding, "A")