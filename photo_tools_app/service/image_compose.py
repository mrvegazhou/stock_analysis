# _*_ coding: utf-8 _*_

from PIL import Image

import sys, os, inspect
PACKAGE_PARENT = '../..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(inspect.getfile(inspect.currentframe())))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from photo_tools_app.exception.api_exception import CreateImgParamFailed
from photo_tools_app.__init__ import utils


class ImageCompose:

    # bgc [255, 255, 255, 1]
    @staticmethod
    def createImage(bgc, width, height):
        is_num = utils['common'].is_num
        if not width or not is_num(width):
            raise CreateImgParamFailed()
        if not height or not is_num(height):
            raise CreateImgParamFailed()

        img = Image.new("RGB", (width, height), bgc)
        return img

    @staticmethod
    def imageResize(img, width, height):
        img_switch = Image.open(img)
        img_deal = img_switch.resize((width, height), Image.ANTIALIAS)
        img_deal.convert('RGBA')
        return img_deal

    '''将图片画在一张图上'''
    @staticmethod
    def drawRectImg(baseImg, img, x, y):
        if not isinstance(baseImg, Image.Image):
            bg_img = Image.open(baseImg).convert('RGBA')
        else:
            bg_img = baseImg.convert('RGBA')
        if not isinstance(img, Image.Image):
            p_img = Image.open(img).convert('RGBA')
        else:
            p_img = img.convert('RGBA')
        r, g, b, a = p_img.split()
        bg_img.paste(p_img, (x, y), mask=a)
        bg_img.convert("RGBA")
        return bg_img


if __name__ == "__main__":
    # img = ImageCompose.createImage((255, 0, 0, 1), 100, 200)
    # img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    # cv2.imshow("white", img)
    # cv2.waitKey(2000)
    img = ImageCompose.drawRectImg('demo1.jpg', 'demo2.png', 12, 15, 20,30)
    # img = img.convert("RGB")
    img.save('tmp.jpg')