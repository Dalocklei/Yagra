#!C:\Python27\python.exe

import cgi
import os
import MySQLdb
import sys
import io

form = cgi.FieldStorage()
message = ""
imagepath = ""

# A nested FieldStorage instance get the username
if form.has_key('username'):
	username = form['username'].value
else:
	username = ""
	message = "ERROR! wrong request format! the username must have a value!"

# Query the image path of this user
if username:
	db = MySQLdb.connect("127.0.0.1","root","","yagra")
	cursor = db.cursor()
	query = "SELECT * FROM user_table WHERE username = '%s'" %(username)
	try:
		cursor.execute(query)
		results = cursor.fetchall()
		if not results:
			message = "The user doesn't exist, the default image will be showed below:"
			imagepath = ""
		else:
			for row in results:
				if not row[2]:	# the user has not uploaded the image
					message = "The user hasn't uploaded his/her image, the default image will be showed below:"
					imagepath = "files/default/default.jpg"			
				else:
					message = "The %s's image is showed below:"%(username)
					imagepath = row[2]
	except:	
		message = "ERROR, unable to query the database!"
	
	db.close()

print "Content-Type: image/jpg\n"
# if your server is on win32, you need to set the stdout mode as binary
if sys.platform == "win32":
	import os, msvcrt
	msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
f = open(imagepath,"rb")
print f.read()