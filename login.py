# Wrote by jialei 2015.03.17  
# Email: leijia_0820@163.com
# Function: login page for Yagra

import cgi
import MySQLdb
import os

header = 'Content-Type: text/html\n\n'
formhtml='''
	<html>
	<body>
	<h1>Welcome to Yagra!</h1>
	<div>
		<form action="./login.py" method="post">
		<INPUT TYPE=hidden NAME=action VALUE=edit>
		User Name: <input type="text" name="user_name"><br />
		Password: <input type="text" name="password" /><br />

		<input type="submit" value="Login" />
		</form>
	</div>
	<div>
		<p>Not Registered?</p>
		<input type="submit" value="Sign Up" onclick="location.href='./signup.py'"/>
	</div>
	</body>
	</html>'''

mainhtml='''
	<html>
	<body>
	<div>
		Login Succeed! Hello %s!
		<input type="submit" value="Log out" onclick="location.href='./login.py'"/>
	</div>
		<H3>Your Image:</H3>
		<img src="./visit_image.py?username=%s" />
	<div>
		<H3>Upload a new image:</H3>
		   <form enctype="multipart/form-data" action="./save_file.py" method="post">
		   <INPUT TYPE=hidden NAME="action" VALUE=%s>
		   <p>Choose an image(only support .jpg/.png/.gif): <input type="file" name="file" /></p>
		   <p><input type="submit" value="Upload" /></p>
		   </form>
	</div>
	</body>'''

errorhtml = '''
	<HTML>
	<BODY>
		<p>%s</p>
		<input type="submit" value="back" onclick="location.href='./login.py'"/>
	</BODY>
	</HTML>'''	
	
def showForm():
    print header + formhtml

def login(username, password):
	if (not username) or (not password):
		if not username:
			print header + errorhtml %("user name is null, please login again!")
		else:
			print header + errorhtml %("password is null, please login again!")			
	else:
		if (os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
			db = MySQLdb.connect(unix_socket='/cloudsql/myyagra:jialei', db='yagra', user='root')
		else:
			db = MySQLdb.connect(host='127.0.0.1', port=3306, db='yagra', user='root')
		cursor = db.cursor()
		query = "SELECT password FROM user_table WHERE username = '%s'" %(username)
		try:
			cursor.execute(query)
			db.commit()
			results = cursor.fetchall()
			if not results:
				print header + errorhtml %("user %s doesn't exist!" %(username))
			else:
				for row in results:
					if row[0] == password:
						print header + mainhtml %(username,username,username)
					else:
						print header + errorhtml %("wrong password! please login again!")					
		except:		
			print header + errorhtml %("error: unable to fetch data!")			
		
		db.close()


def process():
	form = cgi.FieldStorage()
	uname = ''
	upwd = ''
	if form.has_key('user_name'):
		uname = form['user_name'].value
	else:
		uname = ''

	if form.has_key('password'):
		upwd = form['password'].value
	else:
		upwd = ''

	if form.has_key('action'):
		login(uname,upwd)
	else:
		showForm()

if __name__ == '__main__':
	process()
	
