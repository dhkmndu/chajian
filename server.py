#!/usr/env python3
# -*- coding: UTF-8 -*-

from flask import Flask, request, send_file, make_response 
from flask_cors import CORS
import json
import random

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://agents.baidu.com"}})

def make_json_response(data, status_code=200):
    response = make_response(json.dumps(data), status_code)
    response.headers["Content-Type"] = "application/json"
    return response

@app.route("/getCurrentWeather", methods=['GET'])
async def getCurrentWeather():
    """
    获取天气信息
    """
    location = request.args.get('location')
    date = request.args.get('date')

    for data in weather_data:
        if data['location'] == location and data['date'] == date:
            return jsonify(data)

    return jsonify({"message": "找不到对应的天气信息"})



@app.route("/logo.png")
async def plugin_logo():
    """
        注册用的：返回插件的 logo，要求 48 x 48 大小的 png 文件.
        注意：API路由是固定的，事先约定的。
    """
    return send_file('logo.png', mimetype='image/png')


@app.route("/.well-known/ai-plugin.json")
async def plugin_manifest():
    """
        注册用的：返回插件的描述文件，描述了插件是什么等信息。
        注意：API 路由是固定的，事先约定的。
    """
    host = request.host_url
    with open(".well-known/ai-plugin.json", encoding="utf-8") as f:
        text = f.read().replace("PLUGIN_HOST", host)
        return text, 200, {"Content-Type": "application/json"}


@app.route("/.well-known/openapi.yaml")
async def openapi_spec():
    """
        注册用的：返回插件所依赖的插件服务的API接口描述，参照 openapi 规范编写。
        注意：API 路由是固定的，事先约定的。
    """
    with open(".well-known/openapi.yaml", encoding="utf-8") as f:
        text = f.read()
        return text, 200, {"Content-Type": "text/yaml"}

@app.route("/example.yaml")
async def exampleSpec():
    host = request.host_url
    with open("example.yaml") as f:
        text = f.read().replace("PLUGIN_HOST", host)
        return text, 200, {"Content-Type": "text/yaml"}



@app.route('/')
def index():
    return 'welcome to my webpage!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)
