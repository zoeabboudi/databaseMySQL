#!/usr/bin/python

### cgi script here!
from datetime import date, datetime, timedelta

import mysql.connector
from mysql.connector import errorcode

# Import modules for CGI handling 
import cgi, cgitb 

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
title = None
info = None
steal = None
donate_title = 'title of piece'
donate_wing_floor = None
donate_price = 'price'
donate_type = 'type of art'
donate_year_made = 'year made'
donate_artistFN = 'first name'
donate_artistLN = 'last name'
artist_dob = None
artist_dod = None
artist_category = None
category_name = 'name'
category_period = 'period'
category_char = None

if form.getvalue('title'):
    title = form.getvalue('title')
    
if form.getvalue('donate_title'):
    donate_title = form.getvalue('donate_title')
if form.getvalue('donate_wing_floor'):
    donate_wing_floor = form.getvalue('donate_wing_floor')
if form.getvalue('donate_type'):
    donate_type = form.getvalue('donate_type')
if form.getvalue('donate_artistFN'):
    donate_artistFN = form.getvalue('donate_artistFN')
if form.getvalue('donate_artistLN'):
    donate_artistLN = form.getvalue('donate_artistLN')
if form.getvalue('donate_year_made'):
    donate_year_made = form.getvalue('donate_year_made')
if form.getvalue('donate_price'):
    donate_price = form.getvalue('donate_price')
    
if form.getvalue('artist_dob'):
    artist_dob = form.getvalue('artist_dob')
if form.getvalue('artist_dod'):
    artist_dod = form.getvalue('artist_dod')
if form.getvalue('artist_category'):
    artist_category = form.getvalue('artist_category')
if form.getvalue('category_name'):
    category_name = form.getvalue('category_name')
if form.getvalue('category_period'):
    category_period = form.getvalue('category_period')
if form.getvalue('category_char'):
    category_char = form.getvalue('category_char')

if form.getvalue('steal'):
    steal = form.getvalue('steal')

if form.getvalue('info'):
    info = form.getvalue('info')

# Member info
if form.getvalue('firstname'):
    firstname = form.getvalue('firstname')
    lastname = form.getvalue('lastname')
elif form.getvalue('firstlast'):
    firstlast = form.getvalue('firstlast')
    array = firstlast.split("-")
    firstname = array[0]
    lastname= array[1]


DB_NAME = 'zabboudi1'
#conecct with the MySQL server
cnx = mysql.connector.connect(user = "zabboudi", password = "iloveyou", host = "localhost", database = "zabboudi1")
cursor = cnx.cursor()

select_reco = ("SELECT artwork.title, artist.first_name,artist.last_name, artwork.year_made "
               "FROM artwork natural join artist "
               "WHERE artwork.artist_id in (SELECT artist_id FROM interested_in natural join artist WHERE interested_in.memb_id in (SELECT memb_id from member WHERE first_name=%s and last_name=%s))")
data_reco = (firstname,lastname)
cursor.execute(select_reco,data_reco)
myList = []
for (row) in cursor:
    artInfo = [""]*4
    artInfo[0] = row[0]
    artInfo[1] = row[1]
    artInfo[2] = row[2]
    artInfo[3] = row[3]
    myList.append(artInfo)

location = ["no", "where"]

if title != None:
    search_by_name = ("SELECT museum_wing.title, museum_wing.floor FROM museum_wing WHERE museum_wing.wing_id in (SELECT wing_id FROM located_in natural join artwork WHERE artwork.title=%s %s)")
    data_search = (title, "")
    cursor.execute(search_by_name,data_search)
    for (row) in cursor:
        location = [""]*2
        location[0] = row[0]
        location[1] = row[1]
        
information = ["no"]       
if info != None:
    search_by_name = ("SELECT artwork.title, artwork.year_made, artist.first_name, artist.last_name, price.value FROM artwork natural join price natural join artist WHERE title = %s %s;")
    data_search = (info, "")
    cursor.execute(search_by_name,data_search)
    for (row) in cursor:
        information = [""]*5
        information[0] = row[0]
        information[1] = row[1]
        information[2] = row[2]
        information[3] = row[3]
        information[4] = row[4]


print "Content-type:text/html\r\n\r\n"
print '<html>'

print '<body text="ffffff" bgcolor = "#80002a">'
print '<fieldset style="border: 2px dashed #D5DE17;">'
print '<form action="Gallery.py" method=get>'
print 'user: '
print '<input type=text value= %s name="firstname">' % (firstname)
print '<input type=text value= %s name="lastname">' % (lastname)
print '<center>'
print '<font size="7" color=#D5DE17>'
print '<strong>Welcome %s %s! </strong>' % (firstname, lastname)
print '<br>'
print '</font>'
print '<font size ="6">'
print '<br>We recommend you check out the following pieces:'
print '</font>'
print '<br>'
print '<br>'

print '<font size="5">'
for i in range(len(myList)):
    print '<i>%s</i> by %s %s, created in the year %s' % (myList[i][0],myList[i][1],myList[i][2],myList[i][3])
    print '<br>'

print '</center>'
print '<br>'
print '<fieldset style="border: 2px dashed #D5DE17; width: 550px">'
print '<p>'
print '<font size="4">'
print '<strong>Locate a piece of art:'
print '<input type=text  name="title">'
print '<input type=submit value="Search">'
print '<br>'

print '<font size="5">'
if title != None:
    if location[0] == "no":
        print '&nbsp;&nbsp;&nbsp;Sorry, <i> %s </i> is not part of our gallery %s' % (title, "")
    else:
        print '&nbsp;&nbsp;&nbsp;<i> %s </i> is located in the <strong> %s </strong> wing on the %s floor' % (title, location[0], location[1])
print '</strong></p>'
print '</fieldset>'
print '<br>'
print '<fieldset style="border: 2px dashed #D5DE17; width: 550px">'
print '<font size="4">'
print '<p><strong>'
print 'Get information on a piece of art:'
print '<input type=text name="info">'
print '<input type=submit value="Search">'
print '<font size="5">'
if info != None:
    if information[0] == "no":
        print '<br> Sorry, <i> %s </i> is not part of our gallery %s' % (info, "")
    else:
        print '<br> &nbsp;&nbsp;&nbsp;<i> %s </i> was created by %s %s in  %s  <br> &nbsp;&nbsp;&nbsp;<i>%s</i> is estimated to be worth $%s' % (info, information[2], information[3], information[1], info, information[4])

print '</fieldset>'
#print '</form>'
#print '<form action="Gallery.py" method=get>'
# a way to add a piece of art
print '<br> <fieldset style="border: 2px dashed #D5DE17; width: 550px">'
print '<font size="4">'
print '<p><strong>'

print 'Donate a piece of art!<br>'
print '<input type=text name="donate_title" value= %s %s >' % (donate_title, "")
print '<input type=text name="donate_type" value= %s %s >' % (donate_type, "")
print '<input type=text name="donate_year_made" value=%s %s>' % (donate_year_made, "")
print '<input type=text name="donate_artistFN" value = %s %s>' % (donate_artistFN, "")
print '<input type=text name="donate_artistLN" value=%s %s>' % (donate_artistLN,"")
print '<input type=text name="donate_price" value=%s %s >' % (donate_price, "")
print '<select name="donate_wing_floor">'
print '<option value = "Second">Mordechai D. Katz Wing of Classcial Art</option>'
print '<option value = "Third">Monique C. Katz Wing of 20th Century Art</option>'
print '</select>'
print '<input type=submit value="DONATE">'

## end form ##
print '</strong></p>'

######## if someone tries to DONATE ##########

if donate_title!=None and donate_title!='title of piece':
    
    # check if the artist of the piece is in database
    print '<br> thanks for donating'
    select_artist = ("SELECT artist_id "
                   "FROM artist "
                   "WHERE artist.first_name = %s and artist.last_name= %s")
    data_artist = (donate_artistFN,donate_artistLN)
    cursor.execute(select_artist,data_artist)
    print '<br> ran SQL'
    artist_id = None
    for row in cursor:
        artist_id = row[0]
    ## if the artist is not in the database, let's add him/her
    if artist_id == None:
        print '<br> This artist is new to our gallery. Let us know a little about %s %s:' %  (donate_artistFN,donate_artistLN)
        print '<br>date of birth<input type=date name="artist_dob" >'
        print '<br>date of death<input type=date name="artist_dod">'
        print '<br> What category does %s %s belong to?' %  (donate_artistFN,donate_artistLN)
        print '<select name="artist_category" value= %s %s>' % (artist_category, "")
        print '<option value = "Classical">Classical</option>'
        print '<option value = "Impressionism">Impressionism</option>'
        print '<option value = "Expressionism">Expressionism</option>'
        print '<option value = "Fauvism">Fauvism</option>'
        print '<option value = "other">other</option>'
        print '</select>'
        print '<input type=submit value="ADD ARTIST">'
        
        #if the category doesnt exist yet, then add it
        print '<br> artist_category is %s %s ' % (artist_category, "")
        print '<br> artist found %s %s ' % (artist_id, "")
      
        if artist_category == "other":
            print 'This category is also new. Tell us about it:'
            print '<input type=text name="category_name" value=%s %s>' % (category_name, "")
            print '<input type=text name="category_period" value=%s %s>' % (category_period,"")
            print '<textarea rows = "5" cols = "60" name = "category_char" value=%s %s>' % (category_char, "")
            print 'Enter characterizations here...'
            print '</textarea><br>'
            print '<input type=submit value="ADD CATEGORY">'
            
            # once someone has submitted a category
            # add the category
    
        if category_period != None and category_period!='period':
            add_category = ("INSERT INTO category"
                            "(name, time_period,characterizations )"
                            "VALUES (%s, %s, %s)")
            data_category1 = (category_name, category_period, category_char)
            cursor.execute(add_category, data_category1)
            print ' <br>SQL added the category'
            artist_category = category_name
            print '<br> this is the category name %s %s ' % (artist_category, "")
        if artist_category != "other" and artist_category != None:   
            # Now, time to add the artist to the database
            add_artist = ("INSERT INTO artist"
                          "(first_name, last_name,dob,dod, category )"
                          "VALUES (%s, %s, %s, %s, %s)")
            data_artist = (donate_artistFN, donate_artistLN, artist_dob, artist_dod, artist_category)
            cursor.execute(add_artist,data_artist)
            print '<br> artist has been added!'
            select_artist = ("SELECT artist_id "
                   "FROM artist "
                   "WHERE artist.first_name = %s and artist.last_name= %s")
            data_artist = (donate_artistFN,donate_artistLN)
            cursor.execute(select_artist,data_artist)
            print '<br> ran SQL'
            artist_id = None
            for row in cursor:
                artist_id = row[0]
            #print '<input type=text name="done">'
            #print '<input type=submit value="DONE">'
    if artist_id != None:
        # Now add the artwork!!!!
        add_art = ("INSERT INTO artwork"
                    "(title,type,year_made,artist_id)"
                     "VALUES ( %s, %s, %s,%s)")

        data_art = (donate_title, donate_type, donate_year_made, artist_id)
        cursor.execute(add_art,data_art)
        print '<br> artwork ADDED!'
        
        # now add the price
        add_price = ("INSERT INTO price"
                     "(art_no, value )"
                     "VALUES ( %s, %s)")
        select_no = ("SELECT * "
                     "FROM artwork "
                     "WHERE title = %s %s")
        data_select = (donate_title, "")
        cursor.execute(select_no, data_select) 
        for (art_no) in cursor:
            num = (art_no[0])

        data_price = (num, donate_price)
        cursor.execute(add_price, data_price)
        print '<br> price added!'
        # now add the location
        add_location = ("INSERT INTO located_in"
                     "(art_no,wing_id)"
                     "VALUES ( %s, %s)")
        select_wing = ("SELECT * "
                  "FROM museum_wing "
                   "WHERE museum_wing.floor = %s %s")
        data_wing = (donate_wing_floor, "")
        cursor.execute(select_wing, data_wing)
        for (wing) in cursor:
            wing_no= (wing[0])
        data_location = (num, wing_no)
        cursor.execute(add_location, data_location)
        print '<br> location added!'
        print '<input type=submit value="DONE">'




            
        
    ## check if artist exists:
    
## if the artist exists, then add the artwork, the price and location.
## if the artist does not exist, then add the artist to a category
## if the category does not exist then add the cateogry

print '</fieldset>'
print '</form>'
print '</body>'

print '</html>'

# Make sure data is committed to the database
cnx.commit()
#select * from Artist

cursor.close()
cnx.close()
