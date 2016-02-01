#! -*- coding: utf-8 -*-
import requests, urllib

class SongDownloader():
	def __init__(self, fmt='json'):
		self.host = 'http://tingapi.ting.baidu.com/v1/restserver/ting'
		self.payload = {}
		self.payload['format'] = fmt
		self.payload['calback'] = ''
		self.payload['from'] = 'webapp_music'

	def search(self, song, artist=None):
		'''
		Search for the SongID of the song (and artist) given
		'''
		payload = {}
		payload['method'] = 'baidu.ting.search.catalogSug'
		payload['query'] = song
		payload = dict(payload, **self.payload)
		r = requests.get(self.host, params=payload)
		songObj = r.json()
		if artist is None:
			if 'song' not in songObj.keys() or songObj['song'] == 0:
				print "Song not found."
				songid = None
			else:
				prompt = '\n'.join([(str(i+1) + '. ' + each['songname'] + ' ' + each['artistname']) for i, each in enumerate(songObj['song'])])
				print 'Songs found:'
				print prompt
				print
				choice = raw_input('Which one are you pursuing?\n')
				try:
					choice = int(choice) - 1
					songid = songObj['song'][choice]['songid']
				except:
					print 'Please enter a valid choice and try again.'
					songid = None

		else:
			for song in songObj['song']:
				if song['artistname'] == artist:
					songid = song['songid']

		return songid


	def download(self, song, artist=None):
		'''
		Download the song according to the songid searched
		'''
		payload = {}
		payload['songid'] = self.search(song, artist)
		if payload['songid'] is not None:
			payload['bit'] = '320'
			payload['method'] = 'baidu.ting.song.downWeb'
			payload = dict(payload, **self.payload)
			r = requests.get(self.host, params=payload)
			jsonObj = r.json()
			#print jsonObj['bitrate']
			bitlinks = [(int(each['file_bitrate']), each['file_link']) for each in jsonObj['bitrate'] if each['file_link'] != '']
			if len(bitlinks) == 0:
				print 'No links found'
				exit(0)
			link = sorted(bitlinks)[0][1]
			#print jsonObj['bitrate']
			#print link
			try:
				print 'Downloading...'
				urllib.urlretrieve(link, './%s.mp3' % song)
				print 'Download finished.'
				return True
			except Exception as e:
				print 'Download failed.'
				print str(e)
		

if __name__ == '__main__':
	sd = SongDownloader()
	song = raw_input('Please enter a song: ').strip()
	sd.download(song.decode('utf8'))