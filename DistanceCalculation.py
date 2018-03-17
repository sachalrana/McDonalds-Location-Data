# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 00:38:39 2017

@author: Sachal
"""

import sqlite3, time
from geopy.distance import vincenty
from geopy.geocoders import Nominatim

start_time = time.time()
count = 767
lst_OtherMcDonalds = []
lst_NYMcDonalds = []
lst_WithinRangeMcDonalds = []
FileOpen = open("Output_Problem2.txt",'w')

geolocator = Nominatim()

db = sqlite3.connect('McD.db')
print "Database connection successful"

cur = db.cursor()
SQLQuery_NearByMCD = '''SELECT STORENUMBER, CITY, LATITUDE, LONGITUDE, STATE from MCDLocations where State = 'NY'
                        or State = 'NJ' or State = 'MA' or State = 'CT' or State = 'OH' or State = 'RI' 
                        or State = 'VT' or State = 'DE' or State = 'NH' or State = 'NY' '''
                        
AllMcDonaldsNearByNY = cur.execute(SQLQuery_NearByMCD)
lst_OtherMcDonalds = AllMcDonaldsNearByNY.fetchall()


cur = db.cursor()
AllNYMcDonalds = cur.execute('''SELECT STORENUMBER, CITY, LATITUDE, LONGITUDE, STATE from MCDLocations where State = 'NY' ''')
lst_NYMcDonalds = AllNYMcDonalds.fetchall()
#
for EachMcD in lst_NYMcDonalds: 
    coord_CurrentMcDonalds = (EachMcD[2],EachMcD[3])
    count -=1
    print "Iterations Left: "+str(count)
    for EachOtherMcD in lst_OtherMcDonalds:
        if EachOtherMcD in lst_WithinRangeMcDonalds:
            pass
        else:
            coord_OtherMcDonalds = (EachOtherMcD[2],EachOtherMcD[3])
            StraightLineDistance = vincenty(coord_CurrentMcDonalds,coord_OtherMcDonalds).miles
            if StraightLineDistance <= 100 and StraightLineDistance != 0:
                lst_WithinRangeMcDonalds.append(EachOtherMcD)
                print "Store#:"+EachMcD[0]+" "+EachMcD[1]+","+EachMcD[4]+" and Store#:"+EachOtherMcD[0]+" "+ \
                               EachOtherMcD[1]+","+EachOtherMcD[4]+" - Distance: "+ str(StraightLineDistance)+" mi\n"
                FileOpen.write("Store#:"+EachMcD[0]+" "+EachMcD[1]+","+EachMcD[4]+" and Store#:"+EachOtherMcD[0]+" "+ \
                               EachOtherMcD[1]+","+EachOtherMcD[4]+" - Distance: "+ str(StraightLineDistance)+" mi\n")

FileOpen.close()
print "Output in txt file in root folder - Output_Problem2.txt"
print "My program took", time.time() - start_time, "to run"

            
        
