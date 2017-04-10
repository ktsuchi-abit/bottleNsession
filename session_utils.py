#!python

'''utilities for session management on bottle'''

import bottle as btl
import hashlib, os, sqlite3
import decodb

DB_FILE=os.path.join('db', 'db.sqlite3')
SALT=b'a_random_string to make stored passwords secure'

#decorator to open and close database
with_db=decodb.DB(DB_FILE)


def session_set(k,v):
    '''setting the value of k as v in the session'''
    s = btl.request.environ['beaker.session']
    s[k]=v
    s.save()


def session_get(k, delete=False):
    '''getting value of k from the session'''
    s = btl.request.environ['beaker.session']
    v=s[k] if k in s else ''
    if delete and k in s:
        del s[k]
    return v



@with_db
def users(**kw):
    return kw['db'].execute('select uid, role from users').fetchall()


def hash_pw(uid, pw):
    '''calculate the hash value for uid and password'''
    a=hashlib.sha1()
    a.update(uid.encode('utf8')+SALT+pw.encode('utf8'))
    return a.hexdigest()


@with_db
def get_role(uid, pw, **kw):
    r = kw['db'].execute('select role from users where uid=? and pw=?', 
                   (uid, hash_pw(uid, pw))).fetchone()
    return r[0] if r is not None else None


def form_get(k):
    '''getting the value of k from the form'''
    return btl.request.forms.get(k)


def logout():
    s = btl.request.environ['beaker.session']
    s.delete()



@with_db
def create_users_tbl(ls, **kw):
    '''create users table and insert users in ls'''
    db=kw['db']
    db.execute('create table users(' \
                 'uid text primary key not null,' \
                 'pw text not null,' \
                 'role text not null)'
           )
    db.executemany('insert into users(uid, pw, role) values(?,?,?)', 
                   ((u,hash_pw(u,p),r) for u,p,r in ls))                       
    db.commit()


@with_db
def insert_user(uid, pw, role, **kw):
    '''insert a user. if uid is already in the db, it returns false'''
    db=kw['db']
    try:
        db.execute('insert into users(uid, pw, role) values(?,?,?)', 
                   (uid, hash_pw(uid, pw), role))
        db.commit()
        return True
    except sqlite3.DatabaseError:
        return False


@with_db
def change_pw(uid, current_pw, new_pw1, new_pw2, **kw):
    '''changing password'''
    if new_pw1 != new_pw2: 
        return (False, 'The two new passwords are different.')
    db=kw['db']
    r = db.execute('select count(*) from users where uid=? and pw=?', 
                   (uid, hash_pw(uid, current_pw))).fetchone()
    if r[0]==0:
        return (False, 'The current password you gave is invalid.')
    else:
        db.execute('update users set pw=? where uid=?', 
                   (hash_pw(uid, new_pw1), uid))
        db.commit()
        return (True, 'The password has been changed.')
