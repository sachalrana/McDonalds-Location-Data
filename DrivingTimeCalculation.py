# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 23:02:06 2017

@author: Sachal
"""

import sqlite3, random, time, urllib, json
from geopy.distance import vincenty
from geopy.geocoders import Nominatim

start_time = time.time()

lst_McDonaldsNewYork_Chosen = []
lst_McDonaldsNewYork_All = []
lst_McDonaldsDistances_Chosen = []
lst_McDonaldsDistances_Location1 = []
lst_McDonaldsDistances_Location2 = []
lst_McDonaldsDistances_Location3 = []

geolocator = Nominatim()

db = sqlite3.connect('McD.db')

cur = db.cursor()

AllNYMcDonalds = cur.execute('''SELECT STORENUMBER, CITY, LATITUDE, LONGITUDE from MCDLocations where State = 'NY' ''')

for EachNYMcDonald in AllNYMcDonalds:
    lst_McDonaldsNewYork_All.append(EachNYMcDonald)

def RoadDistanceCalculation(lt1,lg1,lt2,lg2):
    orig_coord = lt1+","+lg1
    dest_coord = lt2+","+lg2
    
    url = 'http://maps.googleapis.com/maps/api/distancematrix/json?origins=%s'\
      '&destinations=%s'\
       % (orig_coord, dest_coord)

    result = json.load(urllib.urlopen(url))

    driving_distance = result['rows'][0]['elements'][0]['distance']['text']
    
    return driving_distance        


lst_McDonaldsNewYork_Chosen = random.sample(lst_McDonaldsNewYork_All,3) #Picks any 3 McDonald's in New York randomly from DB


LatLng_1 = (lst_McDonaldsNewYork_Chosen[0][2],lst_McDonaldsNewYork_Chosen[0][3]) #Store 1
StoreNumberAndCity_1 = (lst_McDonaldsNewYork_Chosen[0][0],lst_McDonaldsNewYork_Chosen[0][1])

LatLng_2 = (lst_McDonaldsNewYork_Chosen[1][2],lst_McDonaldsNewYork_Chosen[1][3]) #Store 2
StoreNumberAndCity_2 = (lst_McDonaldsNewYork_Chosen[1][0],lst_McDonaldsNewYork_Chosen[1][1])

LatLng_3 = (lst_McDonaldsNewYork_Chosen[2][2],lst_McDonaldsNewYork_Chosen[2][3]) #Store 3
StoreNumberAndCity_3 = (lst_McDonaldsNewYork_Chosen[2][0],lst_McDonaldsNewYork_Chosen[2][1])

print "Pair-1: Store#: " + lst_McDonaldsNewYork_Chosen[0][0]+","+lst_McDonaldsNewYork_Chosen[0][1] + \
                 " || Store#: " + lst_McDonaldsNewYork_Chosen[1][0]+","+lst_McDonaldsNewYork_Chosen[1][1] + \
                " - Rd. Distance = " + RoadDistanceCalculation(LatLng_1[0],LatLng_1[1],LatLng_2[0],LatLng_2[1])
                 
print "Pair-2: Store#: " + lst_McDonaldsNewYork_Chosen[0][0]+","+lst_McDonaldsNewYork_Chosen[0][1] + \
                 " || Store#: " + lst_McDonaldsNewYork_Chosen[2][0]+","+lst_McDonaldsNewYork_Chosen[2][1] + \
                 " - Rd. Distance = " + RoadDistanceCalculation(LatLng_1[0],LatLng_1[1],LatLng_3[0],LatLng_3[1])
                 
print "Pair-3: Store#: " + lst_McDonaldsNewYork_Chosen[1][0]+","+lst_McDonaldsNewYork_Chosen[1][1] + \
                 " || Store#: " + lst_McDonaldsNewYork_Chosen[2][0]+","+lst_McDonaldsNewYork_Chosen[2][1] + \
                 " - Rd. Distance = " + RoadDistanceCalculation(LatLng_2[0],LatLng_2[1],LatLng_3[0],LatLng_3[1])

print "\n\n"

for EachMcD in lst_McDonaldsNewYork_All:
    LatLng_CurrentLocation = (EachMcD[2],EachMcD[3])
    
    Distance_1 = vincenty(LatLng_1,LatLng_CurrentLocation)
    Distance_2 = vincenty(LatLng_2,LatLng_CurrentLocation)
    Distance_3 = vincenty(LatLng_3,LatLng_CurrentLocation)
    
    lst_McDonaldsDistances_Location1.append((Distance_1,EachMcD[0],EachMcD[1],EachMcD[2],EachMcD[3]))
    lst_McDonaldsDistances_Location2.append((Distance_2,EachMcD[0],EachMcD[1],EachMcD[2],EachMcD[3]))
    lst_McDonaldsDistances_Location3.append((Distance_3,EachMcD[0],EachMcD[1],EachMcD[2],EachMcD[3]))
    

DistancesSorted_Location1 = sorted(lst_McDonaldsDistances_Location1)
DistancesSorted_Location2 = sorted(lst_McDonaldsDistances_Location2)
DistancesSorted_Location3 = sorted(lst_McDonaldsDistances_Location3)


for EachItem in DistancesSorted_Location1[1:11]:
    
    driving_distance = RoadDistanceCalculation(LatLng_1[0],LatLng_1[1],EachItem[3],EachItem[4])
 
    print "Straight Line Distance b/w Store#: " + StoreNumberAndCity_1[0] + " " + StoreNumberAndCity_1[1] + \
    " and Store#: " + EachItem[1] + " " + EachItem[2] + " is " + str(EachItem[0]) + "\n Route Distance: " + driving_distance

print "------------------------------------------------------------"

for EachItem in DistancesSorted_Location2[1:11]:
       
        driving_distance = RoadDistanceCalculation(LatLng_2[0],LatLng_2[1],EachItem[3],EachItem[4])
        
        print "Distance b/w Store#: " + StoreNumberAndCity_2[0] + " " + StoreNumberAndCity_2[1] + \
        " and Store#: " + EachItem[1] + " " + EachItem[2] + " is " + str(EachItem[0]) + "\n Route Distance: " + driving_distance

print "------------------------------------------------------------"

for EachItem in DistancesSorted_Location3[1:11]:
        
        driving_distance = RoadDistanceCalculation(LatLng_3[0],LatLng_3[1],EachItem[3],EachItem[4])
        
        print "Distance b/w Store#: " + StoreNumberAndCity_3[0] + " " + StoreNumberAndCity_3[1] + \
    " and Store#: " + EachItem[1] + " " + EachItem[2] + " is " + str(EachItem[0]) + "\n Route Distance: " + driving_distance

print "My program took", time.time() - start_time, "to run"
