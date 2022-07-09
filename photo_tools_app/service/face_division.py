# _*_ coding: utf-8 _*_

import sys, os, inspect
PACKAGE_PARENT = '../..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(inspect.getfile(inspect.currentframe())))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from photo_tools_app.__init__ import CORE_DIR

import base64

from core.extensions.PPHumanSeg.Matting.predict import ArgsObj, main as FaceDivisionLib

from photo_tools_app.config.constant import Constant
from photo_tools_app.utils.common_util import getFileContent

from aip import AipBodyAnalysis
from photo_tools_app.exception.api_exception import FaceDetectionImgFailed

class FaceDivision():

    @staticmethod
    def getBaiDuClient():
        return AipBodyAnalysis(Constant.BAIDU_APP_ID.value, Constant.BAIDU_API_KEY.value, Constant.BAIDU_SECRET_KEY.value)

    @staticmethod
    def baiduFaceDivision(client: AipBodyAnalysis, image_path, options=None):
        image = getFileContent(image_path)
        res = client.bodySeg(image)
        if 'error_msg' in res and res['error_msg']:
            raise FaceDetectionImgFailed()
        foreground = base64.b64decode(res['foreground'])
        with open('rees.jpg', 'wb') as fp:
            fp.write(foreground)

    @staticmethod
    def libFaceDivision():
        pass

if __name__ == "__main__":
    # FaceDivision.baiduFaceDivision(FaceDivision.getBaiDuClient(), 'image1.jpg')
    args = ArgsObj()
    args.cfg = CORE_DIR+'/extensions/PPHumanSeg/Matting/configs/modnet/modnet-mobilenetv2.yml'
    args.image_path = 'image1.jpg'
    args.save_dir = './output/results'
    args.model_path = CORE_DIR+'/extensions/PPHumanSeg/Matting/export_model/modnet-mobilenetv2/modnet-mobilenetv2.pdparams'
    FaceDivisionLib(args)
