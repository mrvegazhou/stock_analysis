# -*- coding: utf-8 -*-

from photo_tools_app.__init__ import send, reqparse, Redprint
from photo_tools_app.utils.jwt_required import jwt_required

parser = reqparse.RequestParser()

api = Redprint(name='idPhoto')


@api.route('/faceDetect', methods=["POST"])
@jwt_required
def faceImgDetect():
    parser.add_argument('platCode')
    args = parser.parse_args(http_error_code=50003)
    return send(10000, data='test')