#!/usr/bin/python

#  This is the main script for this web application
#  It handles CRUD on all entities/relations & appropriate html for user interaction


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
donate_title = 'title'
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
delete_title  = 'title'
delete_wing = None
add_wing_title = 'nothing'
add_wing_floor = 'nothing'
characterizations = None


## If the user submitted this value on form, then retrieve value
if form.getvalue('title'):
    title = form.getvalue('title')
    
    # values to delete or add artwork/wing
if form.getvalue('delete_title') :
    delete_title = form.getvalue('delete_title')
    
if form.getvalue('delete_wing'):
    delete_wing = form.getvalue('delete_wing')
if form.getvalue('add_wing_title'):
    add_wing_title =  form.getvalue('add_wing_title')
if form.getvalue('add_wing_floor'):
    add_wing_floor =  form.getvalue('add_wing_floor')
if form.getvalue('donate_title') and  form.getvalue('donate_title')!= 'title':
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

    # values to add an artist and category
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

    # values to delete or "steal" a piece of art
if form.getvalue('steal'):
    steal = form.getvalue('steal')

    # value to get info on artwork
if form.getvalue('info'):
    info = form.getvalue('info')

    # values for Member info
if form.getvalue('firstname'):
    firstname = form.getvalue('firstname')
    lastname = form.getvalue('lastname')
elif form.getvalue('firstlast'):
    firstlast = form.getvalue('firstlast')
    array = firstlast.split("-")
    firstname = array[0]
    lastname= array[1]

## Connect to database so we can run mySQL statements
DB_NAME = 'zabboudi1'
#conect with the MySQL server
cnx = mysql.connector.connect(user = "zabboudi", password = "iloveyou", host = "localhost", database = "zabboudi1")
cursor = cnx.cursor()

# select recommendations based on member's interest
select_reco = ("SELECT artwork.title, artist.first_name,artist.last_name, artwork.year_made "
               "FROM artwork natural join artist "
               "WHERE artwork.artist_id in (SELECT artist_id FROM interested_in natural join artist WHERE interested_in.memb_id in (SELECT memb_id from member WHERE first_name=%s and last_name=%s))")
data_reco = (firstname,lastname)
cursor.execute(select_reco,data_reco)
myList = []
for (row) in cursor:   # add all the info for each artwork into a 2D list. 
    artInfo = [""]*4
    artInfo[0] = row[0]
    artInfo[1] = row[1]
    artInfo[2] = row[2]
    artInfo[3] = row[3]
    myList.append(artInfo)

location = ["no", "where"]  # check if you've searched for artwork not in gallery

# look for location of artwork
if title != None:
    search_by_name = ("SELECT museum_wing.title, museum_wing.floor FROM museum_wing WHERE museum_wing.wing_id in (SELECT wing_id FROM located_in natural join artwork WHERE artwork.title=%s %s)")
    data_search = (title, "")
    cursor.execute(search_by_name,data_search)
    for (row) in cursor:  # get floor and wing name
        location = [""]*2
        location[0] = row[0]
        location[1] = row[1]

# get info on a specific piece of art
information = ["no"]

if info != None:
    search_by_name = ("SELECT artwork.title, artwork.year_made, artist.first_name, artist.last_name, artwork.type, price.value FROM artwork natural join price natural join artist WHERE title = %s %s;")
    data_search = (info, "")
    cursor.execute(search_by_name,data_search)
    for (row) in cursor:    # gather all of the info into a list
        information = [""]*6 
        information[0] = row[0]  # title
        information[1] = row[1]  # year made
        information[2] = row[2]  # first name of artist
        information[3] = row[3]  # last name of artist
        information[4] = row[4]  # type of art
        information[5] = row[5]  # price of art
        

### get characterizations of member's interests:
select_char = ("SELECT characterizations FROM category WHERE category.name in (SELECT interested_in.category FROM interested_in WHERE interested_in.memb_id in (SELECT member.memb_id FROM member WHERE member.first_name =%s and member.last_name =%s))")
data_char = (firstname,lastname)
cursor.execute(select_char, data_char) #data_char)
for row in cursor:
    characterizations = row[0]

############# BEGIN HTML ################
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

## display recommendations
print '<font size="5">'
for i in range(len(myList)):
    print '<i>%s</i> by %s %s, created in the year %s' % (myList[i][0],myList[i][1],myList[i][2],myList[i][3])
    print '<br>'
    
# include characterizations of this member's interest
print '<font size="4">'
if characterizations != None:
    print '<p> %s %s </p>' % (characterizations, "")
else:
    print 'to get recommendations, go back to home-page and sign up'
print '</center>'
print '<br>'
print '<fieldset style="border: 2px dashed #D5DE17; width: 550px">'
print '<p>'
print '<font size="4">'
print '<strong>Locate a piece of art:'
print '<input type=text  name="title">'
print '<input type=submit value="Search">'
print '<br>'

# display location if someone asked
# if this artwork not found, say so
print '<font size="5">'
if title != None:
    if location[0] == "no":    # if it exists in Gallery
        print '&nbsp;&nbsp;&nbsp;Sorry, <i> %s </i> is not part of our gallery or it has been misplaced and cannot be located %s' % (title, "")
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

# provide info on artwork if someone asked
print '<font size="5">'
if info != None:

    if information[0] != "no":    # if it exists in Gallery
        print '<br> &nbsp;&nbsp;&nbsp;<i> %s </i> is a(n) %s, created by %s %s in  %s  <br> &nbsp;&nbsp;&nbsp;<i>%s</i> is estimated to be worth $%s' % (info, information[4], information[2], information[3], information[1], info, information[5])
    else:
        print '<br> Sorry, <i> %s </i> is not part of our gallery or it has been misplaced %s' % (info, "")

print '</fieldset>'

# a way to add a piece of art
print '<br> <fieldset style="border: 2px dashed #D5DE17; width: 550px">'
print '<font size="4">'
print '<p><strong>'

print 'Donate a piece of art!<br>'
print '<input type=text id ="donate_title" name="donate_title" value= %s %s >' % (donate_title, "")
print '<input type=text name="donate_type" value= %s %s >' % (donate_type, "")
print '<input type=text name="donate_year_made" value=%s %s>' % (donate_year_made, "")
print '<input type=text name="donate_artistFN" value = %s %s>' % (donate_artistFN, "")
print '<input type=text name="donate_artistLN" value=%s %s>' % (donate_artistLN,"")
print '<input type=text name="donate_price" value=%s %s >' % (donate_price, "")
print '<select name="donate_wing_floor">'
print '<option value =None>none selected</option>'
#display all wing  options
select_wing = ("SELECT * "
               "FROM museum_wing ")
cursor.execute(select_wing)
for row in cursor:
    wing_name = row[1]
    floor_num = row[2]
    print '<option value = %s>%s</option>' % (floor_num, wing_name)
print '</select>'
print '<input type=submit value="DONATE">'
print '</strong></p>'

######## if someone tries to DONATE a piece of art##########

if donate_title!=None and donate_title!='title':
    # check if artwork already in database
    select_piece = ("SELECT art_no "
                    "FROM artwork "
                    "WHERE title = %s %s")
    data_piece = (donate_title, "")
    cursor.execute(select_piece, data_piece)
    number = None
    for row in cursor:
        number = row[0]
    if number != None: #if artwork already in Gallery
        print'<br> this artwork is already in database, dont add!!'
        
    else:  # if artwork new to gallery
        
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
            print '<option value =None>none selected</option>'
            #display all category options
            select_category = ("SELECT name "
                       "FROM category ")
            cursor.execute(select_category)
            for row in cursor:
                cat_name = row[0]
                print '<option value = %s>%s</option>' % (cat_name, cat_name)
            print '<option value = "other">other</option>'
            print '</select>'
            print '<input type=submit value="ADD ARTIST">'

            #if the category doesnt exist yet, then add it
            print '<br> artist_category is %s %s ' % (artist_category, "")
            #print '<br> artist found %s %s ' % (artist_id, "")

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
            if artist_category != "other" and artist_category != None and artist_category != 'None':   
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


print '</fieldset>'
print '<br>'

# A way to delete a piece of art
print '<fieldset style="border: 2px dashed #D5DE17; width: 550px">'
print '<p>'
print '<font size="4">'
print '<strong>STEAL A PIECE OF ART'
print '<input type=text  name="delete_title" value= %s %s>' % (delete_title, "")
print '<input type=submit value="Search">'
print '<br>'
print '<br> you  want to steal %s %s !' % (delete_title, "")
if delete_title != None and delete_title != 'title':
    # check if this title exists in the Gallery
    select_piece = ("SELECT art_no "
                    "FROM artwork "
                    "WHERE title = %s %s")
    data_piece = (delete_title, "")
    cursor.execute(select_piece, data_piece)
    number = None
    for row in cursor:
        number = row[0]
    if number == None: #if artwork already missing from Gallery
        print'<br> this is already mising from gallery so not worth risk!!'
        
    else: # if artwork is in  the gallery

        # delete artwork from price listing
        delete = ("DELETE FROM price "
                  "WHERE price.art_no in (SELECT artwork.art_no "
                  "FROM artwork "
                  "WHERE artwork.title = %s %s)")
        data_delete = (delete_title, "")
        cursor.execute(delete, data_delete)
        print '<br> deleted the price'

        # delete artwork from location listing
        delete_location = ("DELETE FROM located_in "
                  "WHERE located_in.art_no in (SELECT artwork.art_no "
                  "FROM artwork "
                  "WHERE artwork.title = %s %s)")
        data_delete = (delete_title, "")
        cursor.execute(delete_location, data_delete)
        print 'deleted the location'

        # delete artwork
        select_artist = ("SELECT artist_id "
                         "FROM artwork "
                         "WHERE title = %s %s")
        data_delete = (delete_title, "")
        cursor.execute(select_artist, data_delete)
        for row in cursor:
            if row[0]:
                art_id = str(row[0])
        print '<br> got the artist_id. it is %s %s' % (art_id, "")
        delete_artwork = ("DELETE FROM artwork "
                          "WHERE title = %s %s")
        print '<br> this is the title %s %s' % (delete_title, "")
        data_delete = (delete_title, "")
        cursor.execute(delete_artwork, data_delete)
        print '<br> ran delete artwork'

        # see if the artist has made any other painting. If not delete artist from database
        print '<br> this is art_id again %s %s' % (art_id, "")
        count_pieces = ("SELECT count(artwork.title) "
                        "FROM artwork "
                        "WHERE artist_id = %s %s")
        data_art_id = (art_id, "")

        cursor.execute(count_pieces, data_art_id)
        print '<br> ran this count SQL'
        for row in cursor:
            num = row[0]
            
        #if the artist has no other pieces then delete artist from list
        print '<br> this is num %s %s' % (num, "")
        if num ==0:
            print '<br> this is the artists only painting'
            delete_artist = ("DELETE FROM artist "
                             "WHERE artist.artist_id = %s %s")
            data_delete = (art_id, "")
            cursor.execute(delete_artwork, data_delete)
        print '<br> you have stolen %s %s !' % (delete_title, "")



#### steps to steal or delete a wing:

## delete the located_in
# insert/update them to the other wing
## delete wing

print '</fieldset>'
print '<br>'

print '<fieldset style="border: 2px dashed #D5DE17; width: 550px">'
print '<p>'
print '<font size="4">'
print 'remove a museum wing'
print '<select name="delete_wing" value= %s %s>' % (delete_wing, "")
print '<option value =None>none selected</option>'
#display all category options
select_wing = ("SELECT * "
               "FROM museum_wing ")
cursor.execute(select_wing)
for row in cursor:
    wing_name = row[1]
    floor_num = row[2]
    print '<option value = %s>%s</option>' % (floor_num, wing_name)
print '</select>'
print '<input type=submit value="DELTE WING">'
print '<br>'
print '<br> you  want to delete %s %s !' % (delete_wing, "")
if delete_wing != None and delete_wing != 'None':         
    #select_located_in = ("SELECT * "
    ##                     "FROM located_in "
     #                    "WHERE wing_id in (SELECT wing_id FROM museum_wing WHERE floor = %s %s)")
    #data = (delete_wing, "")
    #cursor.execute(select_located_in, data)
    #for row in cursor:
      #  print'<br> this is locate in %s %s ' % (row[0], "")

    # set all located_in for this wing to null
    delete_location_action = ("UPDATE located_in "
                   "SET wing_id = NULL "
                   "WHERE wing_id in (SELECT wing_id FROM museum_wing WHERE floor = %s %s)")
    data = (delete_wing, "")
    cursor.execute(delete_location_action, data)
    print '<br> set the appropriate located_ins to null'

    ## now delete wing
    delete_wing_action = ("DELETE FROM museum_wing "
                          "WHERE floor = %s %s")
    data = (delete_wing, "")
    cursor.execute(delete_wing_action, data)
    print '<br> wing has been deleted'


print '</fieldset>'
print '<br>'


# A way to donate/add  a wing
print '<fieldset style="border: 2px dashed #D5DE17; width: 550px">'
print '<p>'
print '<font size="4">'
print '<strong> DONATE A WING!'
print '<br> give your wing a name:'
print '<input type=text  name="add_wing_title" value= %s %s>' % (add_wing_title, "")
print '<br> what floor should your wing be on? type in words:'
print '<input type=text  name="add_wing_floor" value= %s %s>' % (add_wing_floor, "")
print '<input type=submit value="DONATE">'

#if someone has requested to add a wing
if add_wing_title != 'nothing' and add_wing_title != None and add_wing_title != 'None':
    # first check if this wing already exists
    select_wing = ("SELECT wing_id "
                    "FROM museum_wing "
                    "WHERE title = %s %s")
    data_wing = (add_wing_title, "")
    cursor.execute(select_wing, data_wing)
    number = None
    for row in cursor:
        number = row[0]
    if number != None: #if wing title already in Gallery
        print'<br> this wing title is taken so pick a new one'
        
    else:  # if wing title  new to gallery
        add_wing = ("INSERT INTO museum_wing"
                    "(title,floor)"
                     "VALUES ( %s, %s)")

        data_wing1 = (add_wing_title, add_wing_floor)
        print '<br> your wing has been added!'
        print '<br> this is add_wing_title %s %s ' % (add_wing_title, "")
        cursor.execute(add_wing, data_wing1)
        print ('<br> wing has been added!')

print '</fieldset>'

### display all the artwork so everyone can search
print '<br> below are all the pieces of artwork in our Gallery'
select_titles = ("SELECT title "
                 "FROM artwork ")
cursor.execute(select_titles)
for row in cursor:
    print '<br> <i> %s %s </i>' % (row[0], "")

### display all artists that are in Gallery for reference
print '<br> <br> below are all artists featured in Gallery'
select_artist = ("SELECT first_name, last_name, dob, dod, category "
                 "FROM artist ")
cursor.execute(select_artist)
for row in cursor:
    print '<br> %s %s, %s - %s, %s' % (row[0], row[1], row[2], row[3], row[4])

# delete current member from member list
print '<input type=submit value="delete member" name ="delete_member">'
if form.getvalue('delete_member') != None:
    delete_member = ("DELETE FROM member WHERE first_name = %s and last_name = %s ")
    data_member = (firstname,lastname)
    cursor.execute(delete_member, data_member)
    print '<br> you deleted member!'


# close off items  in html
print '</fieldset>'
print '</form>'
print '</body>'

print '</html>'

############ END OF HTML ###########



# Make sure data is committed to the database
cnx.commit()
#select * from Artist

cursor.close()
cnx.close()
