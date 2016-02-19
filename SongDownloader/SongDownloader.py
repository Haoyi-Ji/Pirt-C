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
                        return ret

                link, extension = sorted(bitlinks, key=lambda x: 640 if x[0]=='flac' else int(x[0]))[-1][1:]
                if extension == '':
                    extension = 'mp3'
                if 'songinfo' in jsonObj and 'artist_id' in jsonObj['songinfo']:
                    artistid = jsonObj['songinfo']['ting_uid']
                else:
                    artistid = None

                ret = {
                    'link': link,
                    'extension': extension,
                    'artistid': artistid
                }
                return ret

        return ret


    def getSongList(self, artistid):
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
        
        try:
            retList = [
                {
                'title': each['title'],
                    'artistname': each['author'].split(','),
                    'artistid': each['all_artist_ting_uid'].split(','),
                    'artists': [{'artistname': aname, 'artistid': aid}
                                for aname, aid in zip(each['author'].split(','),
                                                      each['all_artist_ting_uid'].split(','))],
                    'album': each['album_title'],
                    'link': self.getDownloadLink(each['song_id'])
                }
                for each in jsonObj['songlist']
            ]
        except:
            retList = None
            
        return retList
    
        
    def getArtistInfo(self, artistid):
        '''Get artist data'''

        if artistid is None:
            return None
        payload = {
            'method': 'baidu.ting.artist.getInfo',
            'tinguid': artistid
        }
        payload = dict(payload, **self.payload)
        r = requests.get(self.host, params=payload)
        jsonObj = r.json()
        try:
            retDict = {
                'name': jsonObj['name'],
                'birth': jsonObj['birth'],
                'pic': jsonObj['avatar_big'],
                'constellation': jsonObj['constellation'],
                'stature': jsonObj['stature'],
                'weight': jsonObj['weight']
            }
        except:
            retDict = None
        
        return retDict

    
    def getArtistData(self, artistid):
        info = self.getArtistInfo(artistid)
        songlist = self.getSongList(artistid)
        if info is not None and songlist is not None:
            return {
                'info': info,
                'songlist': songlist
            }
        else:
            return None


    def getLyrics(self, songid):
        if songid is None:
            return None, None
        payload = {
            'method': 'baidu.ting.song.lry',
            'songid': songid
        }
        r = requests.get(self.host, params=payload)
        jsonObj = r.json()
        try:
            songname = jsonObj['title']
            lyrics = jsonObj['lrcContent']
            lyrics = [line.split(']')[1] for line in lyrics.strip().split('\n')]
            return songname, lyrics
        except:
            return None, None


    def getSongData(self, songid):
        if songid is None:
            return None

        link = self.getDownloadLink(songid)
        artistid = link['artistid']
        songname, lrc = self.getLyrics(songid)
        img = self.getArtistInfo(artistid)['pic']
        playlink = self.getPlayLink(songname)
        ret = {
            'songid': songid,
            'songname': songname,
            'lrc': lrc,
            'img': img,
            'link': link,
            'playlink': playlink
        }

        return ret


    def getPlayLink(self, songname):
        host = "http://s.music.163.com/search/get"
        payload = {
            'type': 1,
            's': songname,
            'callback': '',
            'limit': 30
        }
        r = requests.get(host, payload)
        j = r.json()
        songlink = j['result']['songs'][0]['audio']

        return songlink