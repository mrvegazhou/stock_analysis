# -*- coding: utf-8 -*-

import os
from photo_tools_app.__init__ import app, send, reqparse, Redprint, request
from photo_tools_app.__init__ import CODE
from photo_tools_app.service.static_pages import StaticPages
from werkzeug.wrappers import Response

api = Redprint(name='page')

@api.route('/img/<staticFile:fileName>', methods=["POST", "GET"])
def imgPage(fileName):
    mdict = StaticPages.getImgTypes()
    imgPath, name, ext = StaticPages.getStaticPageUrl(fileName)
    print(imgPath, '---imgPath--')
    if not os.path.exists(imgPath):
        return send(80008, data=CODE[80008])
    with open(imgPath, 'rb') as f:
        image = f.read()
    return Response(image, mimetype=mdict[ext])