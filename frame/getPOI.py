#! -*- coding: utf-8 -*-
from BMapPOI import BMapPoint

def getPOI():
    poiDict = {
		'BusStop' : '公交站',
		'Subway' : '地铁站',
		'Building' : '写字楼',
		'Mall' : '商场',
		'Attraction' : '旅游景点',
		'Restaurant' : '餐厅',
		'Community' : '小区',
		'PrimarySchool' : '小学',
		'SecondarySchool' : '中学',
		'University' : '大学'
              }


    file = open('FrameAvailPos.txt', 'r').read().split('\n')
    itemList = sorted(poiDict.keys())
    header = file[0] + '\t' + '\t'.join(itemList) + '\n'

    #batch1 = file[1:3000]
    #batch2 = file[3001:6000]
    #batch3 = file[6001:9000]
    #batch4 = file[9001:]
    batch1 = file[9802:11000]
    batch2 = file[11001:]

    g = open('NewPOIResult.txt', 'w')
    #g.write(header)

    for batch in (batch1, batch2):
	result = ''
        for each in batch:
    	    try:
                data = each.split('\t')
                lon = data[-2]
                lat = data[-1]
                p = BMapPoint(lat, lon)
	        poiList = []
	        for key in itemList:
		    poiList.append(p.getPOI(poiDict[key]))
	        result += each + '\t' + '\t'.join([str(poi) for poi in poiList]) + '\n'
		print data[2] + '\t' + data[4] + '\t' + ''.join([str(p) for p in poiList])
 	    except Exception, e:
	        result += each + '\n'
	        print each
	        print str(e) + '\n'
    
	g.write(result)

    g.close()


if __name__ == '__main__':
    getPOI()
