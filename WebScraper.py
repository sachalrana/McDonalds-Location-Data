# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 23:12:57 2017

@author: Sachal
"""

import requests, bs4, sqlite3, re, time
from bs4 import SoupStrainer
from geopy.geocoders import Nominatim

start_time = time.time()

lst_StateURLS = []
lst_Locations = []
lst_tmp = []

geolocator = Nominatim()
FileOpen = open("Invalid.txt",'w')

db = sqlite3.connect('McD.db')
print "Opened database successfully"

cur = db.cursor()

cur.executescript('''DROP TABLE IF EXISTS MCDLocations;
CREATE TABLE IF NOT EXISTS McDLocations (ID INTEGER PRIMARY KEY AUTOINCREMENT, STORENUMBER TEXT NOT NULL, STADDRESS TEXT NOT NULL, 
                                  CITY TEXT NOT NULL, STATE TEXT NOT NULL, ZIPCODE TEXT NOT NULL, LATITUDE TEXT,
                                  LONGITUDE TEXT)''')

print "Table created successfully";

WebAddress = "https://www.menuism.com/restaurant-locations/mcdonalds-21019/us"
myPage = requests.get(WebAddress)
RequiredDiv = SoupStrainer('div', class_="card popular-cities-box")
mysoup = bs4.BeautifulSoup(myPage.content,"lxml", parse_only=RequiredDiv)
PageList = mysoup.find('ul',class_="list-unstyled-links")
lst_Items = PageList.findAll('li')

reg_Latitude = r'((lat=-?\d{1,3}.\d{1,8}))'
reg_Longitude = r'((lng=-?\d{1,3}.\d{1,8}))' 

for lst_Item in lst_Items:
    Locations = lst_Item.find('a')
    try:
     lst_StateURLS.append(Locations['href'])
    except:
        print Locations
        pass
         

print "State Page Processed"

for EachState in lst_StateURLS:
    McDonaldPage = requests.get(EachState)
    RequiredDiv1 = SoupStrainer('div', class_="card popular-cities-box")
    McDonaldSoup = bs4.BeautifulSoup(McDonaldPage.content,"lxml", parse_only=RequiredDiv1)
    McDonaldList = McDonaldSoup.find('ul',class_="list-unstyled-links")
 
    lst_MCDLocations = McDonaldList.findAll('a')

    for eachitem in lst_MCDLocations:
        lst_Locations.append(eachitem['href'])
        
print "Links Done"

for EachLocation in lst_Locations[:20]:
    LocationPage = requests.get(EachLocation)
    OnlySpanTags = SoupStrainer('div',class_='map-avatar') #To reduce the search space for faster parsing 
    LocationSoup = bs4.BeautifulSoup(LocationPage.content,"lxml",parse_only=OnlySpanTags) 
        
    StoreNumber = re.match('.*?([0-9]+)$', EachLocation).group(1)
    Loc_StreetAddress = LocationSoup.find('span', itemprop="streetAddress").getText().strip()
    Loc_City = LocationSoup.find('span', itemprop="addressLocality").getText().strip()
    Loc_State = LocationSoup.find('span', itemprop="addressRegion").getText().strip()
    Loc_ZipCode = LocationSoup.find('span', itemprop="postalCode").getText().strip()
    LatLng = LocationSoup.find('div',class_='map-background').get('data-bg')
    
    try:
        Loc_Longitude = re.search(r'((lng=-?\d{1,3}.\d{1,8}))',LatLng).group(0)
        Loc_Latitude = re.search(r'((lat=-?\d{1,3}.\d{1,8}))',LatLng).group(0)
    except:
         pass   

    if "lng" in Loc_Longitude or "lat" in Loc_Latitude:
        Loc_Longitude = Loc_Longitude[4:]
        Loc_Latitude = Loc_Latitude[4:]
        
    if Loc_Longitude is None or Loc_Latitude is None:
        try:
            GetLatLng = geolocator.geocode(Loc_StreetAddress+" "+Loc_City+" "+Loc_State+" "+Loc_ZipCode)
            Loc_Longitude = GetLatLng.longitude
            Loc_Latitude = GetLatLng.latitude
        except:
            FileOpen.write(Loc_StreetAddress + " " + Loc_City + " " + Loc_State + " " + Loc_ZipCode+"\n")
            pass
        
    if Loc_ZipCode == "":
        try:
            print "Zip Code Not found"
            GetAddress = geolocator.reverse(Loc_Latitude+","+Loc_Longitude)
            Loc_ZipCode = GetAddress.address.split(",")[-2].strip()
        except:
            pass
        
    if Loc_Longitude and Loc_Latitude:
        myTuple = (StoreNumber,Loc_StreetAddress,Loc_City,Loc_State,Loc_ZipCode,Loc_Longitude,Loc_Latitude)
        
    elif Loc_Longitude and Loc_Latitude and Loc_StreetAddress and Loc_ZipCode is None:
        myTuple = (StoreNumber,"Not Found",Loc_City,Loc_State,"Not Found","Not Found","Not Found")
    
    lst_tmp.append(myTuple)    
    

    print Loc_State #To Keep Track of State currently scrapping and inserting into DB
    
FileOpen.close()
cur.executemany(''' INSERT INTO MCDLocations (STORENUMBER, STADDRESS, CITY, STATE, ZIPCODE, LONGITUDE, LATITUDE) VALUES (?,?,?,?,?,?,?) ''', lst_tmp)
db.commit()
print "Scrapping Complete"
print "My program took", time.time() - start_time, "to run"