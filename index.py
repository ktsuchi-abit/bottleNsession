# -*- coding: utf-8 -*-
 
import os
import bottle as btl
from bottle import run,error,static_file
from bottle import TEMPLATE_PATH, jinja2_template as template
from auth import Auth
import session_utils as ut
from beaker.middleware import SessionMiddleware

DEBUG=True


session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 1000,
    'session.data_dir': './data',
    'session.auto': True
}
app = SessionMiddleware(btl.app(), session_opts)

Auth.config(get_role_from_db=ut.get_role)

# decorators for access controll
req_admin=Auth(role='admin', message='Only admin users can access this page.')
req_login=Auth()

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

@btl.get('/login')
@btl.view('login')
def login_form():
    return {'message':ut.session_get('message', True)}

@btl.post('/login')
@btl.view('login')
def login():
    uid,pw = [ut.form_get(x) for x in ('uid', 'pw')]
    if Auth.login(uid,pw):
        ut.session_set('message', 'こんにちは、{} さん'.format(uid))
        return btl.redirect('/top')
    else:
        return {'message':'ID か Password が間違っています。'}

@btl.route('/logout')
def logout():
    Auth.logout()
    return btl.redirect('/login')

@btl.route('/user')
@req_admin
@btl.view('users')
def users():
    return {'users':ut.users()}


@btl.get('/user/add')
@req_admin
@btl.view('add_user')
def add_user_form():
    return {'message':ut.session_get('message', True)}


@btl.post('/user/add')
@req_admin
@btl.view('add_user')
def add_user():
    r=ut.insert_user(*[ut.form_get(x) for x in ('uid', 'pw', 'role')])
    if r:
        ut.session_set('message', 'add user done.')
        btl.redirect('/')
    else:
        return {'message':'add user failed. try again.'}

    
@btl.get('/user/pw')
@req_login
@btl.view('change_pw')
def change_pw_form():
    return {'message':ut.session_get('message', True)}


@btl.post('/user/pw')
@req_login
@btl.view('change_pw')
def change_pw():
    uid=ut.session_get('uid')
    current_pw, new_pw1, new_pw2 = [ut.form_get(x) for x in ('current_pw', 'new_pw1', 'new_pw2')]    
    b, msg = ut.change_pw(uid, current_pw, new_pw1, new_pw2)
    if b:
        ut.session_set('message', msg)
        btl.redirect('/')
    else:
        return {'message':msg} 
TOP="/top"
@btl.route(TOP)
@req_login
@btl.view(template('index',name="main1"))
def top():
    return {'message':ut.session_get('message', True),
            'role':Auth.get_role()}
 #   return template('index', name="main1")

@btl.route('/top2')
def top2():
    return template('index2',name="main2")
 
if __name__ == "__main__":
    run(app=app,host="localhost", port=8080, debug=DEBUG, reloader=DEBUG)