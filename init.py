#!python

'''create db and insert an admin user'''


import session_utils as ut

ut.create_users_tbl(
    [('peter', 'norvig', 'admin'), ('john', 'smith', 'guest')])
