# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 13:22:39 2016

@author: user
"""

from twython import Twython
import json
import datetime
import os

import mapnik

os.getcwd()
os.chdir("/home/user/git/Twitter")
os.getcwd()

##codes to access twitter API. 
APP_KEY = "4UVISHUjOibJfJR5bQJmxtYkn"
APP_SECRET = "AKyPHV1ky4rqHmIJsPMV9mhrbMSgI4xU3Ele5lAyUAv5UwbZhL"
OAUTH_TOKEN =  "4832215341-J0zwYg1ESDEyoYM9fxDzM5R6POxzHBJ15OPxFIG"
OAUTH_TOKEN_SECRET = "ENVf4s16wacOV1lFikbkF8ELJGtgtpgnnciDCpQ2tUiWJ"

##initiating Twython object 
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

# setting some parameters
latitude =  52.02273	# geographical centre of search
longitude = 5.398135 	# geographical centre of search
max_range = 500 		# search range in kilometres

geo_WS = "%f,%f,%dkm" % (latitude, longitude, max_range)

# first search
search_results_WS = twitter.search(q='#Feyenoord', geocode=geo_WS, count=100)

for result in search_results_WS['statuses']:
    print result
    
##parsing out 
for tweet in search_results_WS["statuses"]:
    username =  tweet['user']['screen_name']
    followers_count =  tweet['user']['followers_count']
    tweettext = tweet['text']
    if tweet['coordinates'] != None:
        full_place_name = tweet['place']['full_name']
        place_type =  tweet['place']['place_type']    
    coordinates = tweet['coordinates']
    if coordinates != None:
        print 'COORDINATES AVAILABLE!!'
        #do it yourself: enter code her to pull out coordinate     
    print username
    print followers_count
    print tweettext
    print coordinates
    #add some some output statements that print lat lon if present
    posted_Tw = tweet['created_at']
    print posted_Tw
    
    
    print '==========================='

dir_output = "./output"

if not os.path.exists(dir_output):
    os.makedirs(dir_output)

output_file = './output/Tweets_Feyenoord.csv'


target = open(output_file, 'w')
target.write('LAT')
target.write('*')
target.write('LON')
target.write('*')
target.write('Time')
target.write('*')
target.write('Followers')
target.write('*')
target.write('Username')
target.write('*')
target.write('TweetText')
target.write('\n')


target.close()


##parsing out 
for tweet in search_results_WS["statuses"]:
    
    target = open(output_file, 'a')
    
    coordinates = tweet['coordinates']
    lat_Tw = coordinates[u'coordinates'][1]
    lon_Tw = coordinates[u'coordinates'][0]
    target.write(str(lat_Tw))
    target.write('*')
    target.write(str(lon_Tw))
    target.write('*')
    
    time_Tw = tweet['created_at'][11:19]
    target.write(time_Tw)
    target.write('*')
    
    followers_count =  tweet['user']['followers_count']
    target.write(str(followers_count))
    target.write('*')

    username =  tweet['user']['screen_name']
    target.write(username)
    target.write('*')

    tweettext = tweet['text']
    target.write(tweettext)
    #target.write('*')
    
    full_place_name = tweet['place']['full_name']
    place_type =  tweet['place']['place_type']
     
    target.write('\n')
    target.close()
    
    print '==========================='
print "DONE!"

print coordinates[u'coordinates']
print tweet['created_at'][11:19]
print coordinates[u'coordinates'][1]


## ASCII to Shapefile

# import libraries
import shapefile, csv

# funtion to generate a .prj file
def getWKT_PRJ (epsg_code):
 import urllib
 wkt = urllib.urlopen("http://spatialreference.org/ref/epsg/{0}/prettywkt/".format(epsg_code))
 remove_spaces = wkt.read().replace(" ","")
 output = remove_spaces.replace("\n", "")
 return output
 
getWKT_PRJ(4326)

# create a point shapefile
tweets_shp = shapefile.Writer(shapefile.POINT)

# for every record there must be a corresponding geometry.
tweets_shp.autoBalance = 1

# create the field names and data type for each.
tweets_shp.field("LATWGS84", "C")
tweets_shp.field("LONWGS84", "C")
tweets_shp.field("TIME", "C")
tweets_shp.field("FOLLOWERS", "C")
tweets_shp.field("USERNAME", "C")
tweets_shp.field("TWEETTEXT", "C")

# count the features
counter = 1

# access the CSV file
#with open('./output/Trees.csv', 'rb') as csvfile:
with open('./output/Tweets_Feyenoord.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter='*')
    # skip the header
    next(reader, None)
    for row in reader:
        latTW = row[0]
        lonTW = row[1]
        timeTW = row[2]
        followersTW = row[3]
        usernameTW = row[4]
        tweettextTW = row[5]
        
        tweets_shp.point(float(lonTW),float(latTW))
        tweets_shp.record(latTW, lonTW, timeTW, followersTW, usernameTW, tweettextTW)

print "Feature " + str(counter) + " added to Shapefile."
 counter = counter + 1

# save the Shapefile
tweets_shp.save("C:/csv_to_shp/Fingal_Trees")

# create a projection file
prj = open("C:/csv_to_shp/Fingal_Trees.prj", "w")
epsg = getWKT_PRJ("4326")
prj.write(epsg)
prj.close()




# http://gis.stackexchange.com/questions/35593/using-the-python-shape-library-pyshp-how-to-convert-csv-file-to-shp
import shapefile as shp
import csv

out_file = './output/GPS_Pts.shp'

#Set up blank lists for data
x,y,time,followers,username,tweettext=[],[],[],[],[],[]

#read data from csv file and store in lists
with open('./output/Tweets_Feyenoord.csv', 'rb') as csvfile:
    r = csv.reader(csvfile, delimiter='*')
    for i,row in enumerate(r):
        if i > 0: #skip header
            x.append(float(row[1]))
            y.append(float(row[0]))
            time.append(row[2])
            followers.append(row[3])
            username.append(row[4])
            tweettext.append(row[5])
 
#Set up shapefile writer and create empty fields
w = shp.Writer(shp.POINT)
w.autoBalance = 1 #ensures gemoetry and attributes match
w.field('X','F',10,8)
w.field('Y','F',10,8)
w.field('Time','C',50)
w.field('Followers','I',10)
w.field('Username','C', 50)
w.field('TweetText','C', 255)

#loop through the data and write the shapefile
for j,k in enumerate(x):
    w.point(k,y[j]) #write the geometry
    w.record(k,y[j],time[j], followers[j], username[j], tweettext[j]) #write the attributes

#Save shapefile
w.save(out_file)

# create a projection file
prj = open("./output/GPS_Pts.prj", "w")
epsg = getWKT_PRJ("4326")
#epsg = getWKT_PRJ("28992")
prj.write(epsg)
prj.close()