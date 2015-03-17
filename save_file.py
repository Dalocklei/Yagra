#!C:\Python27\python.exe

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
if (fext == '.jpg') or (fext == '.jpeg') or (fext == '.png') or (fext == '.bmp') or (fext == '.gif'):
	# Test if the file was uploaded
	if fileitem.filename:
		# strip leading path from file name to avoid directory traversal attacks
		fn = os.path.basename(fileitem.filename)
		filepath = 'files/' + username + fext
		open(filepath, 'wb').write(fileitem.file.read())	# upload the image to the files directory

		# update the image path in Database
		db = MySQLdb.connect("127.0.0.1","root","","yagra")
		cursor = db.cursor()
		query = "UPDATE user_table SET image_path = '%s' WHERE username = '%s'" %(filepath,username)
		try:
			cursor.execute(query)
			results = cursor.fetchall()			
		except:		
			message = 'failed to update the database'			
		
		db.close()
		
		message = 'The file "' + fn + '" was uploaded successfully'
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
""" % (message,)