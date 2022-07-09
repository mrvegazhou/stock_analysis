# _*_ coding: utf-8 _*_

import sys, os, inspect
PACKAGE_PARENT = '../..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(inspect.getfile(inspect.currentframe())))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from photo_tools_app.__init__ import CORE_DIR
sys.path.append(CORE_DIR+'/extensions/face_sdk')
# sys.path.append('/Users/vega/workspace/codes/py_space/working/photo-tools-api/core/extensions/face_sdk')

from aip import AipFace
import yaml
import cv2
import torch
from core.extensions.face_sdk.core.model_loader.face_detection.FaceDetModelLoader import FaceDetModelLoader
from core.extensions.face_sdk.core.model_handler.face_detection.FaceDetModelHandler import FaceDetModelHandler

from photo_tools_app.config.constant import Constant
from photo_tools_app.exception.api_exception import FaceDetModelParseeFailed, FaceDetModelLoaderFailed, FaceDetectionImgFailed


class FaceDetect():

    @staticmethod
    def getBaiDuClient():
        return AipFace(Constant.BAIDU_APP_ID.value, Constant.BAIDU_API_KEY.value, Constant.BAIDU_SECRET_KEY.value)

    @staticmethod
    def baiduFaceDetect(client: AipFace, image, options=None):
        if options:
            return client.detect(image, image_type='BASE64', options=options)
        else:
            return client.detect(image, image_type='BASE64')

    @staticmethod
    def getLibFaceDetection():

        with open(CORE_DIR+'/extensions/face_sdk/config/model_conf.yaml') as f:
            model_conf = yaml.safe_load(f)

        # common setting for all model, need not modify.
        # model_path = CORE_DIR+'/extensions/face_detect/face_sdk/models'
        model_path = 'models'
        # model setting, modified along with model
        scene = 'non-mask'
        model_category = 'face_detection'
        model_name = model_conf[scene][model_category]
        try:
            faceDetModelLoader = FaceDetModelLoader(model_path, model_category, model_name)
        except Exception as e:
            raise FaceDetModelParseeFailed(e)

        try:
            model, cfg = faceDetModelLoader.load_model()
        except Exception as e:
            raise FaceDetModelLoaderFailed(e)

        return model, cfg

    @staticmethod
    def libFaceDetection(model, cfg, image_path):
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        faceDetModelHandler = FaceDetModelHandler(model, 'cuda:0' if torch.cuda.is_available() else 'cpu', cfg)
        try:
            dets = faceDetModelHandler.inference_on_image(image)
            print(dets, '-----')
        except Exception as e:
            raise FaceDetectionImgFailed(e)
        return dets



if __name__ == "__main__":

    model, cfg = FaceDetect.getLibFaceDetection()
    dets = FaceDetect.libFaceDetection(model, cfg, '/Users/zhouquan/Downloads/视频文件/qrcode_for_gh_02e8118151f5_258.jpeg')

