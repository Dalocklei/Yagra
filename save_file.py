#!C:\Python27\python.exe
# Wrote by jialei 2015.03.17  
# Email: leijia_0820@163.com
# Function: Save the file uploaded by user

import cgi
import os
import MySQLdb
import cgitb; cgitb.enable()

try: # Windows needs stdio set for binary mode.
	import msvcrt
	msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
	msvcrt.setmode (1, os.O_BINARY) # stdout = 1
except ImportError:
	pass

form = cgi.FieldStorage()

# A nested FieldStorage instance holds the file
fileitem = form['file']
username = form['action'].value

# Test if the file is an image
fname, fext = os.path.splitext(fileitem.filename)
if (fext == '.jpg') or (fext == '.png') or (fext == '.gif'):
	# Test if the file was uploaded
	if fileitem.filename:
		# strip leading path from file name to avoid directory traversal attacks
		image = fileitem.file.read()
		# update the image blob in Database
		if (os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
			db = MySQLdb.connect(unix_socket='/cloudsql/myyagra:jialei', db='yagra', user='root')
		else:
			db = MySQLdb.connect(host='127.0.0.1', port=3306, db='yagra', user='root')
		cursor = db.cursor()
		query = "UPDATE user_table SET image = %s WHERE username = %s"
		try:
			cursor.execute(query,(image,username))
			db.commit()
		except Error as e:		
			message = 'Failed to update the database'			
		finally:
			db.close()
			message = 'The file was uploaded successfully! Please return back and REFRESH the web page!'
	else:
		message = 'No file was uploaded'
else:
	message = 'please choose an image file!'
   
print """\
Content-Type: text/html\n
<html><body>
<p>%s</p>
click<input type="submit" value="here" onclick="window.history.back()"/>to return back!
</body></html>
""" % (message)