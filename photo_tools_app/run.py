# -*- coding: utf-8 -*-
from __init__ import app, WEB_IP, WEB_PORT, Blueprint, RedprintAssigner

APP_NAME = 'photo_tools_app'

def load_config():
    app.config.from_object('{}.{}.{}'.format(APP_NAME, 'config', 'setting'))

def register_blueprint():
    app.config.from_object('{}.{}.{}'.format(APP_NAME, 'config', 'swagger'))
    assigner = RedprintAssigner(app=app, rp_api_list=app.config['ALL_RP_API_LIST'], api_path='{}.{}'.format(APP_NAME, 'controller'))

    # 将红图的每个api的tag注入SWAGGER_TAGS中
    # @assigner.handle_rp
    # def handle_swagger_tag(api):
    #     app.config['SWAGGER_TAGS'].append(api.tag)

    bp_list = assigner.create_bp_list()
    for url_prefix, bp in bp_list:
        app.register_blueprint(bp, url_prefix=url_prefix)

@app.before_request
def befor_process():
    print("befor_process0")


if __name__ == "__main__":
    load_config()
    register_blueprint()

    if WEB_IP == 'localhost':
        # 本地调试
        app.run(host='0.0.0.0', port=WEB_PORT, debug=False, threaded=True)
        # app.run()
        # ssl_context = (
        #    './server.crt',
        #    './server_nopwd.key')
    else:
        from werkzeug.contrib.fixers import ProxyFix

        # 线上服务部署  对接gunicorn
        app.wsgi_app = ProxyFix(app.wsgi_app)
