#! -*- coding: utf-8 -*-
import requests, urllib

class SongDownloader():
    def __init__(self, fmt='json'):
        self.host = 'http://tingapi.ting.baidu.com/v1/restserver/ting'
	self.payload = {
            'format': fmt,
            'calback': '',
            'from': 'webapp_music'
        }

    def search(self, query):
        '''Search for the SongID of the song (and artist) given'''
        payload = {
            'method': 'baidu.ting.search.catalogSug',
            'query': query
        }
        payload = dict(payload, **self.payload)
        r = requests.get(self.host, params=payload)
        jsonObj = r.json()
        if 'song' not in jsonObj or len(jsonObj['song']) == 0:
            resList = None    # Result not found
        else:
            resList = [dict({'songid': each['songid'],
                            'songname': each['songname'],
                            'artistname': each['artistname']
                            }, **self.getDownloadLink(each['songid']))
                        for each in jsonObj['song']]

            '''
            resList = [(each['songid'], each['songname'], each['artistname']) +
                        self.getDownloadLink(each['songid'])
                        for each in jsonObj['song']]
            '''
        return resList


    def getDownloadLink(self, songid, artist=None):
        '''Download the song according to the songid searched'''
        ret = {
            'link': None,
            'extension': None,
            'artistid': None
        }

        payload = {}
        payload['songid'] = songid
        if payload['songid'] is not None:
            payload['bit'] = 'flac'
            payload['method'] = 'baidu.ting.song.downWeb'
            payload = dict(payload, **self.payload)
            r = requests.get(self.host, params=payload)
            jsonObj = r.json()
            if 'bitrate' in jsonObj:
                bitlinks = [(each['file_bitrate'], each['file_link'], each['file_extension'])
                            for each in jsonObj['bitrate'] if each['file_link'] != '']
                if len(bitlinks) == 0:
                    bitlinks = [(each['file_bitrate'], each['show_link'], each['file_extension']) 
                                for each in jsonObj['bitrate'] if each['show_link'] != ''
                                and ('mp3' in each['show_link'] or 'flac' in each['show_link'])]
                    if len(bitlinks) == 0:
                        return ret #(None,)

                link, extension = sorted(bitlinks, key=lambda x: 640 if x[0]=='flac' else int(x[0]))[-1][1:]
                if extension == '':
                    extension = 'mp3'
                if 'songinfo' in jsonObj and 'artist_id' in jsonObj['songinfo']:
                    artistid = jsonObj['songinfo']['artist_id']
                else:
                    artistid = None

                ret = {
                    'link': link,
                    'extension': extension,
                    'artistid': artistid
                }
                return ret

        return ret


    def getArtistData(self, artistid):
        '''Get song list of the artist'''
        if artistid is None:
            return None
        payload = {
            'method': 'baidu.ting.artist.getSongList',
            'tinguid': artistid,
            'limits': 10,
            'use_cluster': 1,
            'order': 2
        }
        payload = dict(payload, **self.payload)
        r = requests.get(self.host, params=payload)
        jsonObj = r.json()
        
        
