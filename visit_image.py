#!C:\Python27\python.exe
# Wrote by jialei 2015.03.18  
# Email: leijia_0820@163.com
# Function: provide the api for visit image

import cgi
import os
import MySQLdb
import sys
import io
import urllib

form = cgi.FieldStorage()
error = "true"

# A nested FieldStorage instance get the username
if form.has_key('username'):
	username = form['username'].value
else:
	username = ""
	error = "false"

# if your server is on win32, you need to set the stdout mode as binary
if sys.platform == "win32":
	import os, msvcrt
	msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
# Default image to show
default = open("./default.jpg","rb").read()

# Query the image path of this user
if username:
	if (os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
		db = MySQLdb.connect(unix_socket='/cloudsql/myyagra:jialei', db='yagra', user='root')
	else:
		db = MySQLdb.connect(host='127.0.0.1', port=3306, db='yagra', user='root')
	cursor = db.cursor()
	query = "SELECT * FROM user_table WHERE username = '%s'" %(username)
	try:
		cursor.execute(query)
		db.commit()
		results = cursor.fetchall()
		if not results:
			# The user doesn't exist, there will be no image showed
			error = "false"
		else:
			for row in results:
				if not row[2]:
					# The user hasn't uploaded his/her image, the default image will be showed below:"
					image = default			
				else:
					# OK, The image is showed below:
					image = row[2]
	except:
		# Error: there will be no image to show
		error = "false"
	
	db.close()

print "Content-Type: image/jpg\n"
if error != "false":
	print image