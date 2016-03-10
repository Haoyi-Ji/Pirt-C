#! -*- coding: utf-8 -*-
import requests, urllib, time

class SongDownloader():
    def __init__(self):
        self.header = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/search/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'
        }


    def search(self, query):
        '''Search for the SongID of the song (and artist) given'''
        retDict = {
            'song': self.search_for_song(query),
            #'artist': self.search_for_artist(query),
            #'album': self.search_for_album(query)
        }

        return retDict


    def search_for_song(self, query, stype=1, offset=0, total='true', limit=60):
        action = 'http://music.163.com/api/search/get'
        data = {
            's': query,
            'type': stype,
            'offset': offset,
            'total': total,
            'limit': limit
        }

        r = requests.post(action, data=data, headers=self.header)
        jsonObj = r.json()
        songList = jsonObj['result']['songs']
        retList = [{'songid': each['id'], 'songname': each['name'],
                    'songdetail': self.getSongDetail(each['id']),
                    'albumid': each['album']['id'],
                    'albumname': each['album']['name'],
                    #'albumdetail': self.getAlbumDetail(each['album']['id']),
                    'artists': [{'artistid': artist['id'],
                                 'artistname': artist['name'],
                                 #'artistdetail': self.getArtistDetail(artist['id'])
                                 }
                                for artist in each['artists']]}
                    for each in songList]

        return retList


    def search_for_artist(self, query, stype=100, offset=0, total='true', limit=60):
        action = 'http://music.163.com/api/search/get'
        data = {
            's': query,
            'type': stype,
            'offset': offset,
            'total': total,
            'limit': limit
        }

        r = requests.post(action, data=data, headers=self.header)
        jsonObj = r.json()
        retList = jsonObj['result']['artists']

        return retList


    def search_for_album(self, query, stype=10, offset=0, total='true', limit=60):
        action = 'http://music.163.com/api/search/get'
        data = {
            's': query,
            'type': stype,
            'offset': offset,
            'total': total,
            'limit': limit
        }

        r = requests.post(action, data=data, headers=self.header)
        jsonObj = r.json()
        retList = jsonObj['result']['albums']

        return retList


    def getSongDetail(self, songid):
        action = 'http://music.163.com/api/song/detail'
        data = {
            'id': songid,
            'ids': '[' + str(songid) + ']'
        }

        r = requests.get(action, params=data, headers=self.header)
        jsonObj = r.json()

        return jsonObj['songs'][0]


    def getSongData(self, songid):
        data = self.getSongDetail(songid)
        data['lyric'] = self.getLyrics(songid)

        return data


    def getArtistDetail(self, artistid):
        action = 'http://music.163.com/api/artist/' + str(artistid)
        data = {
            'id': artistid,
            'top': 50,
            'ext': 'true'
        }

        r = requests.get(action, params=data, headers=self.header)
        jsonObj = r.json()

        return jsonObj


    def getAlbumDetail(self, albumid):
        action = 'http://music.163.com/api/album/' + str(albumid)
        data = {
            'ext': 'true'
        }
        try:
            r = requests.get(action, params=data, headers=self.header)
            j = r.json()
            '''
            if j['album']['publishTime']:
                j['album']['publishTime'] = self._unix2time(j['album']['publishTime'])
                print j['album']['publishTime']
            '''
            return j['album']
        except:
            return []


    def getLyrics(self, songid):
        action = 'http://music.163.com/api/song/lyric'
        payload = {
            'os': 'osx',
            'id': songid,
            'lv': -1,
            'kv': -1,
            'tv': -1
        }

        try:
            r = requests.get(action, params=payload, headers=self.header)
            j = r.json()
            if j['lrc']['lyric'] != None:
                lyric_info = j['lrc']['lyric']
            else:
                lyric_info = '未找到歌词'
            return [each.split(']')[-1] for each in lyric_info.split('\n')]
        except:
            return []

    '''
    def unix2time(utime):
        u = int(str(utime)) / 1000
        v = time.localtime(u)
        format = '%Y-%m-%d'
        return time.strftime(format, v)
    '''
