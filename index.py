# -*- coding: utf-8 -*-

import os,sys
import bottle as btl
from bottle import run,error,static_file
from bottle import TEMPLATE_PATH, jinja2_template as template
from auth import Auth
import session_utils as ut
from beaker.middleware import SessionMiddleware
import configparser
import re

#iniファイル読み込み
inifile = configparser.SafeConfigParser()
inifile.read('./config.ini', encoding='utf-8')

redirectUrl = inifile.get('settings', 'app_top_dir')
RELOADER=inifile.get('settings', 'RELOADER')
DEBUG=inifile.get('settings', 'DEBUG')

#トップURLの最後の/を削除
appUrl = re.sub("/$", "", redirectUrl)

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 1000,
    'session.data_dir': './data',
    'session.auto': True
}
app = SessionMiddleware(btl.app(), session_opts)

Auth.config(get_role_from_db=ut.get_role)

# decorators for access controll
req_admin=Auth(appUrl, role='admin', message='Only admin users can access this page.')
req_login=Auth(appUrl)

# index.pyが設置されているディレクトリの絶対パスを取得
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# テンプレートファイルを設置するディレクトリのパスを指定
TEMPLATE_PATH.append(BASE_DIR + "/views")

@error(404)
def error404(error):
    return 'Nothing here, sorry'

@btl.route('/static/css/<filename:path>')
def static_css(filename):
    return static_file(filename, root=STATIC_DIR+"/css")

@btl.get(appUrl + "/login")
@btl.view(template('login', appUrl=appUrl))
def login_form():
    return {'message':ut.session_get('message', True)}

@btl.post(appUrl + "/login")
@btl.view(template('login', appUrl=appUrl))
def login():
    uid,pw = [ut.form_get(x) for x in ('uid', 'pw')]
    if Auth.login(uid, pw):
        #ut.session_set('message', 'こんにちは、{} さん'.format(uid))
        #ut.session_set('uid', 'こんにちは、{} さん'.format(uid))
        return btl.redirect(redirectUrl)
    else:
        return {'message':'ID か Password が間違っています。'}

@btl.route(appUrl + '/logout')
def logout():
    Auth.logout()
    return btl.redirect(appUrl + '/login')

@btl.route(appUrl + '/user')
@req_admin
#@btl.view('users')
def users():
    return template('users',
                    users=ut.users(),
                    appUrl=appUrl,
                    message=ut.session_get('message', True),
                    role=Auth.get_role())


@btl.get(appUrl + '/user/add')
@req_admin
#@btl.view('add_user')
def add_user_form():
    return template('add_user',
                    appUrl=appUrl,    
                    message=ut.session_get('message', True),
                    role=Auth.get_role())


@btl.post(appUrl + '/user/add')
@req_admin
@btl.view('add_user')
def add_user():
    r=ut.insert_user(*[ut.form_get(x) for x in ('uid', 'pw', 'role')])
    if r:
        ut.session_set('message', 'add user done.')
        btl.redirect(redirectUrl)
    else:
        return {'message':'add user failed. try again.'}

    
@btl.get(appUrl + '/user/pw')
@req_login
#@btl.view(template('change_pw', appUrl=appUrl))
def change_pw_form():
    return template('change_pw', 
            appUrl=appUrl,
            message=ut.session_get('message', True),
            role=Auth.get_role())

@btl.post(appUrl + '/user/pw')
@req_login
#@btl.view(template('change_pw', appUrl=appUrl))
def change_pw():
    uid=ut.session_get('uid')
    current_pw, new_pw1, new_pw2 = [ut.form_get(x) for x in ('current_pw', 'new_pw1', 'new_pw2')]    
    #print("current_pw="+current_pw+" new_pw1="+new_pw1+" new_pw2="+ new_pw2)
    b, msg = ut.change_pw(uid, current_pw, new_pw1, new_pw2)
    if b:
        print("OK "+uid)
        ut.session_set('message', msg)
        btl.redirect(redirectUrl)
    else:
        print("NG "+uid)

        return template('change_pw', 
                        appUrl=appUrl,
                        message=msg,
                        role=Auth.get_role())

#TOPページ
@btl.route(redirectUrl)
@req_login
#@btl.view(template('index', name="main1", redirectUrl=redirectUrl, appUrl=appUrl))
def top():
#    return {'message':ut.session_get('message', True),
#            'role':Auth.get_role()}
    return template('index', 
                    uid=ut.session_get('uid'),
                    name="main1", 
                    redirectUrl=redirectUrl, 
                    appUrl=appUrl,
                    message=ut.session_get('message', True),
                    role=Auth.get_role())

 #   return template('index', name="main1")

@btl.route(appUrl + '/top2')
@req_login
#@btl.view(template('index2', name="main2", redirectUrl=redirectUrl, appUrl=appUrl))
def top2():
    return template('index2', 
                    name="main2", 
                    redirectUrl=redirectUrl, 
                    appUrl=appUrl,
                    message=ut.session_get('message', True),
                    role=Auth.get_role())

if __name__ == "__main__":
    run(app=app,host="localhost", port=8080, debug=DEBUG, reloader=RELOADER)