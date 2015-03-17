#!C:\Python27\python.exe

import cgi
import MySQLdb

header = 'Content-Type: text/html\n\n'

formhtml = '''<HTML>
<HEAD><TITLE>Sign Up</TITLE></HEAD>
<BODY><H3>New User</H3>
<FORM ACTION="/cgi-bin/signup.py">
<INPUT TYPE=hidden NAME=action VALUE=edit>
User Name:   <INPUT TYPE=text NAME=user_name SIZE=15><br />
Password:    <INPUT TYPE=text NAME=user_passwd_1  SIZE=15><br />
Password again:<INPUT TYPE=text NAME=user_passwd_2  SIZE=15><br />
<INPUT TYPE=submit value="GO"></FORM>
</BODY></HTML>'''

def showForm():
    print header + formhtml

resulthtml = '''<HTML><HEAD><TITLE></TITLE></HEAD>
<BODY>
<p>%s</p>
<input type="submit" value="back" onclick="location.href='/cgi-bin/login.py'"/>
</BODY></HTML>'''

#signup function
def signup(uname, pwd1, pwd2):
	if (not uname) or (not pwd1) or (not pwd2):
		if not uname:
			print header + reshtml %("user name is null, please sign up again!")
		else:
			print header + reshtml %("password is null, please sign up again!")			
	elif (pwd1 != pwd2):
		print header + reshtml %("two password are not the same, please sign up again!")
	else:	# insert into database
		db = MySQLdb.connect("127.0.0.1","root","","yagra")
		cursor = db.cursor()
		query = "SELECT username FROM user_table WHERE username = '%s'" %(uname)
		try:
			cursor.execute(query)
			results = cursor.fetchall()
			if not results:
				sql = "INSERT INTO user_table(username, password) VALUES('%s', '%s')" %(uname, pwd1)
				try:
					cursor.execute(sql)
					db.commit()
				except:
					db.rollback()

				print header + reshtml %("Sign Up Success!")
			else:
				print header + reshtml %("Already have this username, please sign up again!")
		except:		
			print header + reshtml %("error: unable to fetch data!")			
		
		db.close()
		



def process():
	form = cgi.FieldStorage()
	uname = ''
	upwd1 = ''
	upwd2 = ''
	if form.has_key('user_name'):
		uname = form['user_name'].value
	else:
		uname = ''

	if form.has_key('user_passwd_1'):
		upwd1 = form['user_passwd_1'].value
	else:
		upwd1 = ''
		
	if form.has_key('user_passwd_2'):
		upwd2 = form['user_passwd_2'].value
	else:
		upwd2 = ''

	if form.has_key('action'):
		signup(uname,upwd1,upwd2)
	else:
		showForm()

if __name__ == '__main__':
	process()
