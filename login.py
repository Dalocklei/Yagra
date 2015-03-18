#!C:\Python27\python.exe

import cgi
import MySQLdb

header = 'Content-Type: text/html\n\n'
formhtml='''
	<html>
	<body>
	<h1>Welcome to Yagra!</h1>
	<div>
		<form action="/cgi-bin/login.py" method="post">
		<INPUT TYPE=hidden NAME=action VALUE=edit>
		User Name: <input type="text" name="user_name"><br />
		Password: <input type="text" name="password" /><br />

		<input type="submit" value="Login" />
		</form>
	</div>
	<div>
		<p>Not Registered?</p>
		<input type="submit" value="Sign Up" onclick="location.href='/cgi-bin/signup.py'"/>
	</div>
	</body>
	</html>'''

mainhtml='''
	<html>
	<body>
	<div>
		Login Succeed! Hello %s!
		<input type="submit" value="Log out" onclick="location.href='/cgi-bin/login.py'"/>
	</div>
		<H3>Your Image:</H3>
		<img src="/cgi-bin/visit_image.py?username=%s" />
	<div>
		<H3>Upload a new image:</H3>
		   <form enctype="multipart/form-data" action="/cgi-bin/save_file.py" method="post">
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
		<input type="submit" value="back" onclick="location.href='/cgi-bin/login.py'"/>
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
		db = MySQLdb.connect("127.0.0.1","root","","yagra")
		cursor = db.cursor()
		query = "SELECT password FROM user_table WHERE username = '%s'" %(username)
		try:
			cursor.execute(query)
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
	
