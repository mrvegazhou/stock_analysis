# _*_ coding: utf-8 _*_

from enum import Enum, unique

@unique
class Constant(Enum):
    # 微信·小程序
    APP_ID = 'wx551ff8259cd7339b'
    APP_SECRET = '7773e41929841faf6aa9e68807f6e2cb'
    WX_LOGIN = 'https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code'

