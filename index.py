# -*- coding: utf-8 -*-
 
import os
from bottle import route, run,error,static_file
from bottle import TEMPLATE_PATH, jinja2_template as template
 
# index.pyが設置されているディレクトリの絶対パスを取得
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# テンプレートファイルを設置するディレクトリのパスを指定
TEMPLATE_PATH.append(BASE_DIR + "/views")

@error(404)
def error404(error):
    return 'Nothing here, sorry'

@route('/static/css/<filename:path>')
def static_css(filename):
    return static_file(filename, root=STATIC_DIR+"/css")

@route('/top')
def top():

    return template('index', name="main1")

@route('/top2')
def top2():
    return template('index2',name="main2")
 
if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True, reloader=True)