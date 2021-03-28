#!/usr/bin/python

import cgi, cgitb
form = cgi.FieldStorage()
account = form.getvalue('username')
password = form.getvalue('password')

print ("Hello, account is %s and password is %s" % (account, password))