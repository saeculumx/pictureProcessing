import cv2
import numpy as np
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')


def img_bw(path):
    """
    Function import pictures and turn into black/white picture for more processing
    :param path: path to the picture
    :return: picture save in middle folder
    """

    """Grey Picture"""

    image_r = Image.open(path)
    b = image_r.filename.split("/")[-1]
    print(">>IMP<< Reading {}".format(b))
    img_grey = image_r.convert('L')
    img_grey.save("middle/grey_" + b)
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
    th_pic.save("middle/thd_" + b)
    th_avg_pic.save("middle/thd_avg_" + b)
    print(">>IMP<< Picture {} Has been Processed (Two)".format(b))
    plt.show()
    """Eroded"""
    image_f = cv2.imread("middle/thd_" + b)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
    eroded_img = cv2.erode(th1, kernel)
    cv2.imwrite("middle/eroded {}".format(b), eroded_img)
    eroded_img_dim = 255 - eroded_img
    contours, hierarchy = cv2.findContours(eroded_img_dim, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    color = (255,255,255)
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
        print(hierarchy)
        cv2.imwrite("result/res_{}_".format(i) + b, temp)
        cv2.imwrite("final/f_" + b, temp)
        cv2.imwrite("middle/parameter_{}_".format(i) + b, image_f)
        i = i + 1

    # cv2.imwrite("final/" + str(x_a[-2]) + b, t_a[-1])
