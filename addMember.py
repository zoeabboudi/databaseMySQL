#!/usr/bin/python

#from __future__ import print_function
from datetime import date, datetime, timedelta

import mysql.connector
from mysql.connector import errorcode

# Import modules for CGI handling 
import cgi, cgitb 


# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
firstname = form.getvalue('firstname')
lastname  = form.getvalue('lastname')

year = int(form.getvalue('year'))
month  = int(form.getvalue('month'))
day  = int(form.getvalue('day'))

interest = form.getvalue('interest')


print "Content-type:text/html\r\n\r\n"
print '<html>'
#print '<body background="/smile.png" width="100%" height="100%">'
print '<body text="ffffff" bgcolor = "#80002a">'

print '<br/>'
print '<center>'
#print '<title>'
print '<font size="7">'
print '<img src="smile.png">'
print '<strong> Congrats!</strong><br>'
print '</font>'
print '<font size ="6">'
print ' %s %s is now a member!' % (firstname, lastname)
print '<br>'
print '<br>'
print '<form action="Gallery.py" method=get>'
print '<button style="height:50px;width:200px" type="submit" name="firstlast" value=%s-%s >Proceed to Virtual Art Gallery</button>' % (firstname, lastname)
print '</form>'
print '</font>'
print '</center>'
print '<br/>'
print '<br/>'

print '</body>'
print '</html>'



DB_NAME = 'zabboudi1'
#conecct with the MySQL server
cnx = mysql.connector.connect(user = "zabboudi", password = "iloveyou", host = "localhost", database = "zabboudi1")
cursor = cnx.cursor()

add_member = ("INSERT INTO member"
                "(first_name, last_name,dob )"
                 "VALUES ( %s, %s, %s)")
data_member1 = (firstname, lastname, date(year,month,day))
#write to the screen that they were successfully signed up!

cursor.execute(add_member, data_member1)

# Now we need to add their interests into Interested_In
add_interest = ("INSERT INTO interested_in"
                "(memb_id,category)"
                 "VALUES ( %s, %s)")
select_id = ("SELECT *"
             "FROM member")
cursor.execute(select_id) 
for (memb_no) in cursor:
    if memb_no[1] == firstname:
        num1 = (memb_no[0])
data_inter = (num1, interest)
cursor.execute(add_interest, data_inter)

# Make sure data is committed to the database
cnx.commit()
#select * from Artist

cursor.close()
cnx.close()

