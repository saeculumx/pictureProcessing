import string

import concatenateImages
import fileGenerator
import importPics
from string import ascii_lowercase as alc
from string import ascii_uppercase as ulc

if __name__ == '__main__':
    filetype = ".png"
    font = "arial.ttf"


    # concatenateImages.words_to_picture(font, "This is a: *[Example]* ,.?")

    def generate_cut():
        for punc in string.punctuation:
            text = str(ord(punc))
            fontname = "punc"
            print(">>GEN<< : Punc is : {} || ".format(ord(punc)) + punc)
            src_fontname = "punc"
            filename = text + "_" + src_fontname + filetype
            print(filename)
            fileGenerator.generate_pics(128, 128, text, fontname, 90, capital="capital")
            importPics.img_bw("generate/{}".format("punc" + "_capital" + "/" + filename), capital="capital")
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


    #generate_cut()
    concatenateImages.words_to_picture(font, "This is a:\n *[Example]* ,.?")
