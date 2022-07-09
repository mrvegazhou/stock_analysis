# -*- coding: utf-8 -*-
from photo_tools_app.__init__ import APIException
from photo_tools_app.__init__ import CODE


class WeChatException(APIException):
    res_code = 70000
    msg = CODE[70000]
    http_code = 500
    data = ''

class JWTExpiredSignatureError(APIException):
    res_code = 20007
    msg = CODE[20007]
    http_code = 401
    data = ''

class JWTDecodeError(APIException):
    res_code = 20006
    msg = CODE[20006]
    http_code = 401
    data = ''

class JWTInvalidTokenError(APIException):
    res_code = 20008
    msg = CODE[20008]
    http_code = 401
    data = ''

class FaceDetModelParseeFailed(APIException):
    def __init__(self, data):
        self.data = data
    res_code = 80001
    msg = CODE[80001]
    http_code = 401

class FaceDetModelLoaderFailed(APIException):
    def __init__(self, data):
        self.data = data
    res_code = 80002
    msg = CODE[80002]
    http_code = 401

class FaceDetectionImgFailed(APIException):
    def __init__(self, data):
        self.data = data
    res_code = 80003
    msg = CODE[80003]
    http_code = 401


