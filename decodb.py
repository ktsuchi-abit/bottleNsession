#!python

'''
a decorator to access sqlite3 databases

the db connection is passed to the modifying function
via a keyword parameter 

===== example =====
with_db=decodb.DB(DB_FILE)

@with_db
def users(**kw):
    return kw['db'].execute('select uid, role from users').fetchall()

'''


import os, sqlite3

class DB:
    '''generating decorators to access sqlite3 database '''
    def __init__(self, dbfile, parm_name='db'):
        self.dbfile=dbfile
        self.parm_name=parm_name
        dir=os.path.dirname(dbfile)
        if dir and not os.path.isdir(dir):
            os.makedirs(dir)
        
    def __call__(self, fun):
        '''acting as a decorator'''
        def _f(*a, **k):
                db=sqlite3.connect(self.dbfile)
                k[self.parm_name]=db
                try: return fun(*a, **k)
                finally: db.close()
                
        return _f
