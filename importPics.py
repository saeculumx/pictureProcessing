import cv2
import numpy as np
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
from pathlib import Path

matplotlib.use('TkAgg')


def img_bw(path, capital):
    """
    Function import pictures and turn into black/white picture for more processing
    :param capital: if the text is capital
    :param path: path to the picture
    :return: picture save in middle folder
    """

    """Grey Picture"""
    """Grey Picture"""

    image_r = Image.open(path)
    b = image_r.filename.split("/")[-1]
    font = image_r.filename.split("/")[-2]
    # print(b,font)
    if "." in font:
        fontname = font.split(".")[0]
    else:
        fontname = font.split("_")[0]
    print(">>SMP<< Reading {}".format(b + "//" + fontname + "//" + font))
    img_grey = image_r.convert('L')
    Path("middle/" + capital).mkdir(parents=True, exist_ok=True)
    img_grey.save("middle/" + capital + "/grey_" + b)
    print(">>IMP<< Picture {} Has been Processed (Grey)".format(b))

    """B&W Picture"""
    """B&W Threshold pre"""
    print(">>IMP<< Reading {}".format(b))
    two = cv2.imread(path)
    two = cv2.cvtColor(two, cv2.COLOR_RGB2GRAY)
    two = cv2.medianBlur(two, 5)
    """Fixed"""
    ret, th1 = cv2.threshold(two, 127, 255, cv2.THRESH_BINARY)
    """Mean thd"""
    th2 = cv2.adaptiveThreshold(two, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    """Gaussian thd"""
    th3 = cv2.adaptiveThreshold(two, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    """Display"""
    titles = ['Original Image', 'Global Thresholding (v = 127)', 'Adaptive Mean Thresholding',
              'Adaptive Gaussian Thresholding']
    images = [two, th1, th2, th3]
    """Draw T Points"""
    for i in range(4):
        plt.subplot(2, 2, i + 1), plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])
    th_pic = Image.fromarray(th1)
    th_avg_pic = Image.fromarray(th3)
    th_pic.save("middle/" + capital + "/thd_" + b)
    th_avg_pic.save("middle/" + capital + "/thd_avg_" + b)
    print(">>IMP<< Picture {} Has been Processed (Two)".format(b))
    # plt.show()
    """Eroded"""
    image_f = cv2.imread("middle/" + capital + "/thd_" + b)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 50))
    eroded_img = cv2.erode(th1, kernel)
    cv2.imwrite("middle/" + capital + "/eroded_{}".format(b), eroded_img)
    eroded_img_dim = 255 - eroded_img
    contours, hierarchy = cv2.findContours(eroded_img_dim, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filename = b.split("_")[-1]
    print(">>IMP<< point at: " + "final/{}".format(fontname) + "/" + capital)
    Path("final/{}".format(fontname) + "/" + capital).mkdir(parents=True, exist_ok=True)
    Path("result/" + capital).mkdir(parents=True, exist_ok=True)
    color = (255, 255, 255)
    x_a = []
    t_a = []
    i = 1
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        # print("RES " + str(x) + str(y) + str(w) + str(h))
        # image_n = np.array(image_f)
        cv2.rectangle(image_f, (x, y), (x + w, y + h), color, 1)
        temp = image_f[y:(y + h), x:(x + w)]
        x_a.append(x)
        t_a.append(temp)
        # print(hierarchy)
        cv2.imwrite("result/" + capital + "/res_{}_".format(i) + b, temp)
        cv2.imwrite("final/{}".format(fontname) + "/" + capital + "/" + b, temp)
        # print(">>RES<< ","final/{}".format(fontname) + "/" + capital + "/" + b)
        cv2.imwrite("middle/" + capital + "/parameter_{}_".format(i) + b, image_f)
        i = i + 1
