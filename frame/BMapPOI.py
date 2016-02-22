# -*- coding:utf-8 -*-
import urllib, urllib2
import json
import numpy as np
from numpy import sin, cos

class BMapPoint():
    def __init__(self, lat, lon):
        self.lat = str(lat)
        self.lon = str(lon)

    def getPOI(self, poi_to_get, r=300):
        poi_dict = {'query': poi_to_get}
        query = urllib.urlencode(poi_dict)
        url_begin = 'http://api.map.baidu.com/place/v2/search?'
        url_end = '&output=json&ak=aQbiXLKYETCsTDSuVmljaBX7&page_size=100'
        location = self.lat + ',' + self.lon
        radius = str(r)
        url = url_begin + query + '&location=' + location + '&radius=' + radius + url_end

        res = urllib2.urlopen(url).read()
        result = json.loads(res)
        N = result['total']

	'''
        itemList = []
        poiList = []
        for each in result['results']:
            print each['name']
            itemList.append(each['name'])
            lon = each['location']['lng']
            lat = each['location']['lat']
            poiList.append((lon, lat))
        if poiList:
            shortestDistance = min([self.getDistanceFrom(each) for each in poiList])
        else:
            shortestDistance = 10**18
	'''

        return N#, shortestDistance

    
    def getDistanceFrom(self, (lon, lat)):
        url_begin = 'http://api.map.baidu.com/direction/v1?mode=walking&origin='
        origin = self.lat + ',' + self.lon
        destination = str(lat) + ',' + str(lon)
        url_end = '&region=%E4%B8%8A%E6%B5%B7&output=json&ak=aQbiXLKYETCsTDSuVmljaBX7'
        url = url_begin + origin + '&destination=' + destination + url_end
        res = urllib2.urlopen(url).read()
        result = json.loads(res)
        if result['message'] == 'ok':
            distance = result['result']['routes'][0]['distance']
            duration = result['result']['routes'][0]['duration']

        return float(distance)


    '''
    def getDistance((lonA, latA), (lonB, latB)):
        EARTH_RADIUS = 6378.137
        
        radlonA = rad(float(lonA))
        radlonB = rad(float(lonB))
        radlatA = np.pi/2.0 - rad(float(latA))
        radlatB = np.pi/2.0 - rad(float(latB))
        #print radlatA, radlatB, radlonA, radlonB
        C = sin(radlatA)*sin(radlatB)*cos(radlonA-radlonB) + cos(radlatA)*cos(radlatB)
        dis = EARTH_RADIUS * np.arccos(C)#*np.pi/180.0
        return dis*1000
    def rad(d):
        return d * np.pi / 180.0
    def getDuration(lonA, latA, lonB, latB):
        rul_header = ''
    '''

    #http://api.map.baidu.com/direction/v1?mode=walking&origin=31.222104,121.38064&destination=31.220447,121.393676&region=%E5%8C%97%E4%BA%AC&output=json&ak=aQbiXLKYETCsTDSuVmljaBX7



if __name__ == '__main__':
    #print getDistance('121.38064', '31.222104', '121.393676', '31.220447')
    #print getDistance('121.38064', '31.222104', '121.365833', '31.223828')
    A = BMapPoint('31.222104','121.38064')
    print A.getPOI('学校')
