import base64
import flask
from flask_app import app
from flask import jsonify, request, render_template
from dataclasses import dataclass, field, asdict
from typing import Any
from settings import Config
from logger import info_log


@dataclass
class ApiResponse:
    code: int = 200
    msg: str = '成功'
    data: Any = field(default_factory=lambda: {})


@app.errorhandler(404)
def S404Handle(error):
    return render_template('404.html'), 404


@app.before_request
def before_request():
    ...


@app.after_request
def after_request(resp: flask.Response):
    if isinstance(resp.data, bytes): return resp

    data = resp.json or resp.data.decode('utf-8')
    status_code = resp.status_code

    if status_code == 404: return resp
    if status_code != 200:
        response = ApiResponse(code=status_code, msg=resp.status, data=data)
    else:
        if data is None: data = {}
        response = ApiResponse(code=200, data=data)

    resp = jsonify(asdict(response))
    return resp


if __name__ == "__main__":
    info_log.info('*****************关键参数配置********************')
    info_log.info('版本：2023.06.01.001')
    info_log.info(f'项目：{Config.PROJECT_NAME}')
    info_log.info(f'环境：{Config.ENV_NAME}')
    info_log.info(f'REDIS地址：{Config.REDIS_HOST}')
    info_log.info(f'MySQL地址：{Config.MYSQL_HOST}')
    info_log.info('***********************************************')

    app.run(host="0.0.0.0", port=Config.PORT, debug=Config.DEBUG)
