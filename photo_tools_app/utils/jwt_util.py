# -*- coding: utf-8 -*-

import jwt
import datetime
from photo_tools_app.config.constant import Constant


class JwtUtil():
    @staticmethod
    def encode_token(data):
        # 构造header
        headers = {
            'typ': 'jwt',
            'alg': 'HS256'
        }
        try:
            # 构造payload
            payload = {
                'iat': datetime.datetime.utcnow(),
                'iss': 'ken',
                'data': data,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)  # 超时时间
            }
            return jwt.encode(payload=payload, key=Constant.JWT_SALT.value, algorithm="HS256", headers=headers)
        except Exception as e:
            return e

    @staticmethod
    def decode_token(auth_token):
        try:
            # payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), leeway=datetime.timedelta(seconds=10))
            # 取消过期时间验证
            payload = jwt.decode(auth_token, Constant.JWT_SALT.value, options={'verify_exp': False})
            if 'data' in payload:
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError as e:
            return e
        except jwt.InvalidTokenError as e:
            return e
