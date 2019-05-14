### This file provides the layout of my database and some sample data featuring my favorite pieces of art. ###

from __future__ import print_function
from datetime import date, datetime, timedelta

import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'zabboudi1'
#conecct with the MySQL server
cnx = mysql.connector.connect(user = "zabboudi", password = "iloveyou", host = "localhost", database = "zabboudi1")
cursor = cnx.cursor()

sql1 = "DROP TABLE IF EXISTS located_in;"
sql2 = "DROP TABLE IF EXISTS museum_wing;"
sql3 = "DROP TABLE IF EXISTS price;"
sql4 = "DROP TABLE IF EXISTS artwork;"
sql5 = "DROP TABLE IF EXISTS interested_in;"
sql6 = "DROP TABLE IF EXISTS member;"
sql7 = "DROP TABLE IF EXISTS artist;"
sql8 = "DROP TABLE IF EXISTS category;"
cursor.execute(sql1)
cursor.execute(sql2)
cursor.execute(sql3)
cursor.execute(sql4)
cursor.execute(sql5)
cursor.execute(sql6)
cursor.execute(sql7)
cursor.execute(sql8)


TABLES = {}

TABLES['category'] = (
    "CREATE TABLE `category` ("
    "  `name` varchar(20),"
    "  `time_period` varchar(16) NOT NULL,"
    "  `characterizations` varchar(255), "
    "  PRIMARY KEY (`name`)"
    ") ENGINE=InnoDB")

TABLES['artist'] = (
    "CREATE TABLE `artist` ("
    "  `artist_id` int(10) NOT NULL AUTO_INCREMENT,"
    "  `first_name` varchar(14),"
    "  `last_name` varchar(16),"
    "  `dob` date,"
    "  `dod` date,"
    "  `category` varchar(20),"
    "  PRIMARY KEY (`artist_id`),"
    "  CONSTRAINT `artist_ibfk_2` FOREIGN KEY (`category`) "
    "     REFERENCES `category` (`name`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES['artwork'] = (
    "CREATE TABLE `artwork` ("
    "  `art_no` int(10) NOT NULL AUTO_INCREMENT,"
    "  `title` varchar(40) NOT NULL,"
    "  `type` varchar(20),"
    "  `year_made` int(4),"
    "  `artist_id` int(10),"
    "  PRIMARY KEY (`art_no`),"
    "  CONSTRAINT `artwork_ibfk_2` FOREIGN KEY (`artist_id`) "
    "     REFERENCES `artist` (`artist_id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES['member'] = (
    "CREATE TABLE `member` ("
    "  `memb_id` int(10) NOT NULL AUTO_INCREMENT,"
    "  `first_name` varchar(20) NOT NULL,"
    "  `last_name` varchar(20) NOT NULL,"
    "  `dob` date NOT NULL,"
    "  PRIMARY KEY (`memb_id`)"
    ") ENGINE=InnoDB")

TABLES['museum_Wing'] = (
    "CREATE TABLE `museum_wing` ("
    "  `wing_id` int(10) NOT NULL AUTO_INCREMENT,"
    "  `title` varchar(20) NOT NULL,"
    "  `floor` varchar(16) NOT NULL,"
    "  PRIMARY KEY (`wing_id`)"
    ") ENGINE=InnoDB")

TABLES['interested_in'] = (
    "CREATE TABLE `interested_in` ("
    "  `memb_id` int(10),"
    "  `category` varchar(20),"
    "  PRIMARY KEY (`memb_id`),"
    "  CONSTRAINT `interested_in_ibfk_2` FOREIGN KEY (`memb_id`) "
    "     REFERENCES `member` (`memb_id`) ON DELETE CASCADE,"
    "  CONSTRAINT `interested_in1_ibfk_2` FOREIGN KEY (`category`) "
    "     REFERENCES `category` (`name`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES['located_in'] = (
    "CREATE TABLE `located_in` ("
    "  `art_no` int(10),"
    "  `wing_id` int(10),"
    "  PRIMARY KEY (`art_no`),"
    "  CONSTRAINT `located_in_ibfk_2` FOREIGN KEY (`art_no`) "
    "     REFERENCES `artwork` (`art_no`) ON DELETE CASCADE,"
    "  CONSTRAINT `located_in1_ibfk_2` FOREIGN KEY (`wing_id`) "
    "     REFERENCES `museum_wing` (`wing_id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")




def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

TABLES['price'] = (
    "CREATE TABLE `price` ("
    "  `art_no` int(10),"
    "  `value` int(12),"
    "  PRIMARY KEY (`art_no`),"
    "  CONSTRAINT `price_ibfk_2` FOREIGN KEY (`art_no`) "
    "     REFERENCES `artwork` (`art_no`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

print("Creating table {}: ".format('price'), end='')
cursor.execute(TABLES['price'])
print("OK")
alter =("ALTER TABLE artwork AUTO_INCREMENT = 100;")
cursor.execute(alter)


add_category = ("INSERT INTO category"
                "(name, time_period,characterizations )"
                "VALUES (%s, %s, %s)")
data_category1 = ( 'Impressionism', '1860-1890', 'Impressionism is characterized by the inclusion of movement as a crucial element of human perception and experience.')
data_category2 = ('Expressionism', '1910-1930', 'Expressionism represents the world based on emotional experience rather than impressions of the external world.')
data_category3 = ('Classical', '500BCE - 200', 'In classical sculpture bodies were highly idealized, but achieved an unprecedented degree of naturalism.')
data_category4 = ('Fauvism', '1904-1910', 'Fauvism emphasized painterly qualities and strong color over representational or realistic qualities.')
cursor.execute(add_category, data_category1)
cursor.execute(add_category, data_category2)
cursor.execute(add_category, data_category3)
cursor.execute(add_category, data_category4)
add_artist = ("INSERT INTO artist"
                "(first_name, last_name,dob,dod, category )"
                "VALUES (%s, %s, %s, %s, %s)")
data_artist1 = ( 'Claude', 'Monet', date(1840,11,14), date(1926,12,5),'Impressionism')
data_artist2 = ('Vincent', 'vanGogh', date(1853,5,30),date(1890,7,29),'Impressionism')
data_artist3 = ('Jackson', 'Pollock', date(1912,1,28),date(1956,8,11),'Expressionism')
data_artist4 = ('Polykleitos', 'None', date(0001, 1, 1), date(0001, 1, 1), 'Classical')
data_artist5 = ('Henri', 'Matisse', date(1869,12,31),date(1954,11,3),'Fauvism')
data_artist6 = ('Michelangelo', 'None', date(1475,5,6),date(1564,2,18),'Classical')
cursor.execute(add_artist, data_artist1)
cursor.execute(add_artist, data_artist2)
cursor.execute(add_artist, data_artist3)
cursor.execute(add_artist, data_artist4)
cursor.execute(add_artist, data_artist5)
cursor.execute(add_artist, data_artist6)

add_member = ("INSERT INTO member"
                "(first_name, last_name,dob )"
                 "VALUES ( %s, %s, %s)")
data_member1 = ('Zoe', 'Abboudi', date(1997,10,6))
data_member2 = ('Isaac', 'Abboudi', date(2001,4,17))
data_member3 = ('Mori', 'Schick', date(1998, 5, 16))
data_member4 = ('Alyssa', 'Wruble', date(1996, 11, 11))
data_member5 = ('Alisha', 'Abboudi', date(1969, 11, 18))
cursor.execute(add_member, data_member1)
cursor.execute(add_member, data_member2)
cursor.execute(add_member, data_member3)
cursor.execute(add_member, data_member4)
cursor.execute(add_member, data_member5)

add_art = ("INSERT INTO artwork"
                "(title,type,year_made,artist_id)"
                 "VALUES ( %s, %s, %s,%s)")
select_id = ("SELECT *"
             "FROM artist")
cursor.execute(select_id) 
for (artist_id) in cursor:
    if artist_id[1] == 'Claude':
        art_id1 = (artist_id[0])
    elif artist_id[1] == 'Henri':
        art_id2 = artist_id[0]
    elif artist_id[1] == 'Jackson':
        art_id3 = artist_id[0]
    elif artist_id[1] == 'Michelangelo':
        art_id4 = artist_id[0]
data_art1 = ('Impression, Sunrise', 'Oil paint', 1872, art_id1)
data_art2 = ('The Joy of Life', 'Oil on canvas', 1906, art_id2)
data_art3 = ('Lavender Mist', 'Oil on canvas', 1950, art_id3)
data_art4 = ('David', 'Sculpture', 1504, art_id4)
cursor.execute(add_art, data_art1)
cursor.execute(add_art, data_art2)
cursor.execute(add_art, data_art3)
cursor.execute(add_art, data_art4)

select_id = ("SELECT *"
             "FROM artist")
cursor.execute(select_id) 
for (artist_id) in cursor:
    if artist_id[1] == 'Vincent':
        art_id = (artist_id[0])
data_art2 = ('Starry Night', 'Oil paint', 1889, art_id)
cursor.execute(add_art, data_art2)

data_art3 = ('Sunflowers', 'Oil paint', 1888, art_id)
cursor.execute(add_art, data_art3)

select_id = ("SELECT *"
             "FROM artist")
cursor.execute(select_id) 
for (artist_id) in cursor:
    if artist_id[1] == 'Polykleitos':
        art_id = (artist_id[0])

data_art4 = ('Doryphoros', 'Sculpture', 500, art_id)
cursor.execute(add_art, data_art4)

add_price = ("INSERT INTO price"
                "(art_no, value )"
                 "VALUES ( %s, %s)")
select_id = ("SELECT *"
             "FROM artwork")
cursor.execute(select_id) 
for (art_id) in cursor:
    if art_id[1] == 'Starry Night':
        num = (art_id[0])

data_price1 = (num, '50000000')
select_id = ("SELECT *"
             "FROM artwork")
cursor.execute(select_id) 
for (art_id) in cursor:
    if art_id[1] == 'Impression, Sunrise':
        num1 = (art_id[0])

data_price2 = (num1, '12500000')
cursor.execute(add_price, data_price1)
cursor.execute(add_price, data_price2)
select_id = ("SELECT *"
             "FROM artwork")
cursor.execute(select_id) 
for (art_id) in cursor:
    if art_id[1] == 'Doryphoros':
        num1 = (art_id[0])

data_price3 = (num1, '99900000')
cursor.execute(add_price, data_price3)

add_wing = ("INSERT INTO museum_wing"
                "(title,floor)"
                 "VALUES ( %s, %s)")

data_wing1 = ('Mordechai D. Katz', 'Second')
data_wing2 = ('Monique C. Katz', 'Third')
data_wing3 = ('Gerald Schottenstein', 'First')
cursor.execute(add_wing, data_wing1)
cursor.execute(add_wing, data_wing2)
cursor.execute(add_wing, data_wing3)


add_location = ("INSERT INTO located_in"
                "(art_no,wing_id)"
                 "VALUES ( %s, %s)")
select_art = ("SELECT *"
             "FROM artwork")
cursor.execute(select_id) 
for (art_no) in cursor:
    if art_no[1] == 'Starry Night':
        num1 = (art_no[0])
    elif art_no[1] == 'Impression, Sunrise':
        num2 = art_no[0]
    elif art_no[1] == 'Doryphoros':
        num3 = art_no[0]
    elif art_no[1] == 'Sunflowers':
        num4 = art_no[0]
    elif art_no[1] == 'David':
        num5 = art_no[0]
    elif art_no[1] == 'The Joy of Life':
        num6 = art_no[0]
select_wing = ("SELECT *"
              "FROM museum_wing")
cursor.execute(select_wing) 
for (wing_id) in cursor:
    if wing_id[2] == 'Third':
        wing3 = (wing_id[0])
    elif wing_id[2] == 'Second':
        wing2 = wing_id[0]
data_location1 = (num1,wing3)
data_location2 = (num2,wing3)
data_location3 = (num3,wing2)
data_location4 = (num4, wing3)
data_location5 = (num5, wing2)
data_location6 = (num6, wing3)
cursor.execute(add_location,data_location1)
cursor.execute(add_location,data_location2)
cursor.execute(add_location,data_location3)
cursor.execute(add_location,data_location4)
cursor.execute(add_location,data_location5)
cursor.execute(add_location,data_location6)


add_interest = ("INSERT INTO interested_in"
                "(memb_id,category)"
                 "VALUES ( %s, %s)")
select_id = ("SELECT *"
             "FROM member")
cursor.execute(select_id) 
for (memb_no) in cursor:
    if memb_no[1] == 'Zoe':
        num1 = (memb_no[0])
    elif memb_no[1] == 'Isaac':
        num2 = memb_no[0]
    elif memb_no[1] == 'Mori':
        num3 = memb_no[0]
    elif memb_no[1] == 'Alyssa':
        num4 = memb_no[0]
    elif memb_no[1] == 'Alisha':
        num5 = memb_no[0]
data_inter = (num1, 'Impressionism')
data_inter1 = (num3, 'Expressionism')
data_inter2 = (num2, 'Classical')
data_inter3 = (num4, 'Fauvism')
data_inter4 = (num5, 'Impressionism')

cursor.execute(add_interest, data_inter)
cursor.execute(add_interest, data_inter1)
cursor.execute(add_interest, data_inter2)
cursor.execute(add_interest, data_inter3)
cursor.execute(add_interest, data_inter4)

         
# Make sure data is committed to the database
cnx.commit()
#select * from Artist

cursor.close()
cnx.close()
