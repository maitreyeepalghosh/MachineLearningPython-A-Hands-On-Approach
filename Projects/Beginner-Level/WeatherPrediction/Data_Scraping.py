
# coding: utf-8
from bs4 import BeautifulSoup
import requests
import re
import string
from geopy.geocoders import Nominatim
from math import radians, cos, sin, asin, sqrt

listData=[]

def remove_non_ascii(text):
    return ''.join([i if ord(i)<128 else '' for i in text])

def getData(url):
    r  = requests.get(url,verify=False)
    data =remove_non_ascii(r.text).decode('unicode_escape').encode('ascii','ignore')
    soup = BeautifulSoup(data,"lxml")
    return soup

def getBangloreGeoLocation():
    cityname='Bangalore'
    geolocator = Nominatim()
    geoLocation = geolocator.geocode(cityname)
    latitude=geoLocation.latitude
    longitude=geoLocation.longitude
    return latitude,longitude

bangLat,bangLong=getBangloreGeoLocation()


def getHaversineDistance(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    distInKm =int(6367 * c)
    return distInKm
    

url='https://www.timeanddate.com/weather/india'

soup=getData(url)

tbody=soup.find('table',attrs={"class" : "zebra fw tb-wt zebra va-m"})
tdList=tbody.find_all('td')

for td in tdList:
    a=td.find('a')
    if a is not None:
        cityname=a.text        
        geolocator = Nominatim()
        geoLocationDest = geolocator.geocode(cityname)
        if geoLocationDest is None:
            continue
        destLat=geoLocationDest.latitude
        destLong=geoLocationDest.longitude        
        distance= getHaversineDistance(destLat,destLong,bangLat,bangLong)
          
        link='https://www.timeanddate.com'+a['href']+'/ext' 
        minTempSum=0
        maxTempSum=0
        humditySum=0
        windSum=0
        weatherPrefCount=0
        
        soup1=getData(link)
        tbody1 = soup1.find('table', id="wt-ext").find('tbody')
        if tbody1 is not None:
            trList=tbody1.find_all('tr')
            if trList is not None:
                for tr in trList:
                    tdList=tr.find_all('td')
                    if tdList is not None and len(tdList)>6:
                        minMaxTemp=tdList[1].text
                        if (minMaxTemp is not None) and (minMaxTemp.find("/") != -1):
                            temp=tdList[1].text.split("/")
                            minTemp=temp[0].strip()
                            minTempSum=minTempSum+int(minTemp)
                            maxTemp=re.sub('[^0-9]','', temp[1].strip())
                            maxTempSum=maxTempSum+int(maxTemp)
                        weather=tdList[2].text
                        if(weather.lower().find('sunny')  or weather.lower().find('more sun') or weather.lower().find('sun')):
                            weatherPrefCount=weatherPrefCount+1
                            
                        wind= tdList[4].text
                        windSum=windSum+int(wind.replace("km/h","").strip())
                        humidity=tdList[6].text 
                        humditySum=humditySum+int(humidity.replace("%",""))                        
        avgMinTemp,avgMaxTemp,avgWind,avgHumidity = minTempSum / 14,maxTempSum/14,windSum/14,humditySum/14
        if(distance<1500 and avgMinTemp>10 and avgMaxTemp<=30 and avgWind<=15 and avgHumidity<=40 and weatherPrefCount>2):
            value=cityname,destLat,destLong,distance,avgMinTemp,avgMaxTemp,avgWind,avgHumidity,"Sunny",1
        else: 
            value=cityname,destLat,destLong,distance,avgMinTemp,avgMaxTemp,avgWind,avgHumidity,"Cloudy",0
        print "*******************",value
        listData.append(value)


import csv
print listData
with open('training data.csv','wb') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['CityName','Latitude (degree)','Longitude (degree)','Distance (km)','Min Temp (°C)','Max Temp (°C)','Wind (km/h)','Humidity (%)','Weather','Target'])
    for row in listData:
        csv_out.writerow(row)




