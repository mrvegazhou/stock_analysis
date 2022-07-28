# _*_ coding: utf-8 _*_

import sys, os, inspect
PACKAGE_PARENT = '../..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(inspect.getfile(inspect.currentframe())))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from photo_tools_app.__init__ import CORE_DIR

import base64

from core.extensions.PPHumanSeg.Matting.infer import ArgsObj, main as FaceDivisionLib

from photo_tools_app.config.constant import Constant
from photo_tools_app.utils.common_util import getFileContent

from aip import AipBodyAnalysis
from photo_tools_app.exception.api_exception import FaceDetectionImgFailed, FaceImgSaveDirFailed, FaceImgNotExists


class FaceDivision(object):

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
    def libFaceDivision(save_dir, image_path):
        if not save_dir or not os.path.isdir(save_dir):
            raise FaceImgSaveDirFailed()
        if not image_path or not os.path.exists(image_path):
            raise FaceImgNotExists()
        args = ArgsObj()
        args.cfg = CORE_DIR + '/extensions/PPHumanSeg/Matting/models/modnet-mobilenetv2/deploy.yaml'
        args.image_path = image_path
        args.save_dir = save_dir
        FaceDivisionLib(args)






if __name__ == "__main__":
    # FaceDivision.baiduFaceDivision(FaceDivision.getBaiDuClient(), 'image1.jpg')
    FaceDivision.libFaceDivision('/Users/vega/workspace/codes/py_space/working/photo-tools-api/photo_tools_app/service/out', '/Users/vega/workspace/codes/py_space/working/photo-tools-api/photo_tools_app/service/p.jpg')
