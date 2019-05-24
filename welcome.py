#!/usr/bin/python
from datetime import date, datetime, timedelta

import mysql.connector
from mysql.connector import errorcode
import cgi, cgitb 

DB_NAME = 'zabboudi1'
#conecct with the MySQL server
cnx = mysql.connector.connect(user = "zabboudi", password = "iloveyou", host = "localhost", database = "zabboudi1")
cursor = cnx.cursor()


print "Content-type:text/html\r\n\r\n"
print '<html>'
#print '<body background="/smile.png" width="100%" height="100%">'
print '<body text="ffffff" bgcolor = "#80002a">'


print '<br/>'
print '<center>'
#print '<title>'
print '<font size="7">'
print '<strong>Welcome </strong><br>'
print '</font>'
print '<font size ="6">'
print 'to our '
print '</font>'
print '<font size = "7">'
print '<strong>Art Gallery</strong>'
#print '</title>'
print '</font>'
print '<img src="../images/smile.png" width = 100px >'
print '</center>'
print '<br/>'
#print '<br/>'

print '<form action="Gallery.py" method=get>'
print '<center>'
print '<font size="5">'
print '<fieldset style="width:270px">'
print '<legend>Member Sign In</legend>'
print 'First name:<br>'
print '<input type=text size=20 name="firstname">'
print '<br>'
print 'Lastname: <br>'
print '<input type=text size=20 name="lastname">'
print '<br> <br>'
print '<input type=submit value="Sign In">'
print '</fieldset>'
print '</font>'
print '</center>'
print '</form>'

print '<br/>'
print '<center>'
print '<form action="addMember.py" method=get>'
print '<font size="4">'
print '<fieldset style="width:270px">'
print '<legend>Sign Up Now</legend>'
print 'First name:<br>'
print '<input type=text size=20 name="firstname">'
print '<br>'
print 'Lastname: <br>'
print '<input type=text size=20 name="lastname">'
print '<br>'
print 'Date of Birth:'
print '<br>'
print '<font size = 2>'
print 'month day   year<br>'
print '<input type=text size=2 name ="month">'
#print 'day'
print '<input type=text size=2 name ="day">'
#print 'year'
print '<input type=text size=4 name ="year">'
print '<br>'
print '<font size = 4>'
print 'Interested In'
print '<select name="interest">'
#display all category options
select_category = ("SELECT name "
           "FROM category ")
cursor.execute(select_category)
for row in cursor:
    cat_name = row[0]
    print '<option value = %s>%s</option>' % (cat_name, cat_name)
#print '<option value = "Impressionism">Impressionism</option>'
#print '<option value = "Expressionism">Expressionism</option>'
#print '<option value = "Fauvism">Fauvism</option>'
#print '<option value = "other">other</option>'
print '</select>'
#print '<option value = "Classical">Classical</option>'
#print '<option value = "Impressionism">Impressionism</option>'
#print '<option value = "Expressionism">Expressionism</option>'
#print '<option value = "Fauvism">Fauvism</option>'
#print '</select>'
print '<br> <br>'

print '<input type=submit value="Sign Up">'
print '</fieldset>'
print '</font>'
print '</center>'
print '</form>'


print '</body>'
print '<body>'


print '</body>'
print '</html>'



# Make sure data is committed to the database
cnx.commit()
#select * from Artist

cursor.close()
cnx.close()
