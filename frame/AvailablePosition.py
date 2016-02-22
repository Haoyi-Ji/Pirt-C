from hivepy import HiveClient
import numpy as np
import pandas as pd

conn = HiveClient()

query = 'select * from Tmp_AnalysisQueryDB.Kevin_FrameAd_AvailablePosition'
res = conn.execute(query)
headers = ['city','id','name','district','address','type','rt1','rt2','rt3','rt4','rt5','rt6','rt7','price','population','height','longitude','latitude']
data = map(lambda s: s.split('\t'), res)
position = pd.DataFrame(data, columns=headers)

query = 'select * from Tmp_AnalysisQueryDB.Kevin_FrameAd_CityRange'
res = conn.execute(query)
headers = ['city','lonfrom','lonto','latfrom','latto']
data = map(lambda s: s.split('\t'), res)
cityRange = pd.DataFrame(data, columns=headers)

query = 'select * from Tmp_AnalysisQueryDB.Kevin_FrameAd_Campaign2014'
res = conn.execute(query)
headers = ['city','startdate','enddate','name','numofads']
data = map(lambda s: s.split('\t'), res)
campaign = pd.DataFrame(data, columns=headers)

cityList = set(city)


def getDataFrame(table):
	query = 'select * from ' + table
	res = conn.execute(query)
	data = map(lambda s: s.split('\t'), res)
	query = 'desc ' + table
	headers = conn.execute(query)
	headers = map(lambda s: s.split('\t')[0].strip(), headers)
	return pd.DataFrame(data, columns=headers)


def main():
	