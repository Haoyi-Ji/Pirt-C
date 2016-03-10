#! -*- coding: utf-8 -*-
import requests, urllib

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
            'song': _search_for_song(query),
            'artist': _search_for_artist(query),
            'album': _search_for_album(query)
        }

        return resDict


    def _search_for_song(query, stype=1, offset=0, total='true', limit=60):
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
                    'songdetail': getSongDetail(each['id']),
                    'albumid': each['album']['id'],
                    'albumid': each['album']['name'],
                    'albumdetail': getAlbumDetail(each['album']['id'])
                    'artists': [{'artistid': artist['id'],
                                 'artistname': artist['name'],
                                 'artistdetail': getArtistDetail(artist['id'])}
                                for artist in each['artists']]
                    for each in songList]
        
        return retList


    def _search_for_artist(query, stype=100, offset=0, total='true', limit=60):
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


    def _search_for_album(query, stype=10, offset=0, total='true', limit=60):
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
            'ids': '[' + songid + ']'
        }

        r = requests.get(action, params=data, headers=self.header)
        jsonObj = r.json()

        return jsonObj['result']
    

    def getArtistDetail(self, artistid):
        action = 'http://music.163.com/api/artist/' + str(artistid)
        data = {
            'id': artistid,
            'top': 50,
            'ext': 'true'
        }

        r = requests.get(action, params=data, headers=self.header)
        jsonObj = r.json()

        return jsonObj['result']


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
                    'songid': each['song_id'],
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
        try:
            j = r.json()
            songlink = j['result']['songs'][0]['audio']
        except:
            songlink = None

        return songlink
