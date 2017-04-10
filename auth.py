#!python

'''
a decorator for acess controll by role

===== example =====
Auth.config(get_role_from_db=ut.get_role)
# decorators for access controll
req_admin=auth.Auth(role='admin', message='Only admin users can access this page.')
req_login=auth.Auth()

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
        return btl.redirect('/')
    else:
        return {'message':'ID か Password が間違っています。'}


@btl.route('/')
@req_login
@btl.view('index')
def index():
    return {'message':ut.session_get('message', True),
            'role':ut.session_get('role')}


@btl.route('/user')
@req_admin
@btl.view('users')
def users():
    return {'users':ut.users()}
'''

import bottle as btl
import session_utils as ut
from functools import partial, wraps

class Auth:
    '''generating decorators for access control'''
       
    # class attribute
    CLS_ATTR=[
      ('get_role_from_db', lambda uid,pw:None), # lambda uid,pw: role if a record having (uid, pw) exists in the db else None 
      ('logout', ut.logout), # method to clear the session
      ('set_uid', partial(ut.session_set, 'uid')), # method to set uid into the session
      ('set_role', partial(ut.session_set, 'role')), # method to set role into the session
      ('get_uid', lambda:ut.session_get('uid')), # method to get uid from the session
      ('get_role', lambda:ut.session_get('role')), # method to get role from the session
      ('set_message', partial(ut.session_set,'message')), 
    ]
    
    @classmethod
    def config(cls, **kw):
        '''setting static methods'''
        for k,v in cls.CLS_ATTR:
            setattr(cls, k, staticmethod(kw.get(k,v)))
            
    @classmethod    
    def login(cls, uid, pw):
        role=cls.get_role_from_db(uid, pw)
        if role:
            cls.set_uid(uid)
            cls.set_role(role)
        return role
        
    def  __init__(self,**kw):
        '''kw parameters are role, message and failure_redirect'''
        for k,v in [('message', 'Login required'), ('failure_redirect', '/login')]:
            setattr(self, k, kw.get(k, v))
        self.is_auth=(lambda :kw['role']==self.get_role()) if 'role' in kw else self.get_role
                            
    def __call__(self, fun):
        '''acting as a decorator'''
        @wraps(fun)
        def _f(*a, **k):
            if self.is_auth():
                return fun(*a, **k)
            else:
                self.set_message(self.message)
                return btl.redirect(self.failure_redirect)
        return _f
