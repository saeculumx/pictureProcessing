import concatenateImages
import fileGenerator
import importPics
from string import ascii_lowercase as alc
from string import ascii_uppercase as ulc

if __name__ == '__main__':
    filetype = ".png"
    font = "CALIBRI.TTF"
    concatenateImages.words_to_picture(font, "For Example This is Aompqg")


    def generate_cut():
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

    # generate_cut()
