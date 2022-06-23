# -*- coding: utf-8 -*-
from photo_tools_app.__init__ import APIException
from photo_tools_app.__init__ import CODE


class WeChatException(APIException):
    res_code = 70000
    msg = CODE[70000]
    http_code = 500
    data = ''




