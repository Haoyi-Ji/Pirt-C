#! -*- coding: utf-8 -*-
import requests, sys
from pprint import pprint

class dictionary():
    def __init__(self):
        self.url = 'http://fanyi.youdao.com/openapi.do'
        self.payload = {
            'keyfrom': 'dictapp',
            'key': '1657096875',
            'type': 'data',
            'doctype': 'json',
            'version': '1.1'
        }

    def translate(self, query):
        self.payload['q'] = query
        r = requests.get(self.url, params=self.payload)
        j = r.json()
        if j['errorCode'] == 0:
            translation = j['translation']
            for each in translation:
                print each
            if 'basic' in j.keys():
                if 'us-phonetic' in j['basic'].keys():
                    print '[' + j['basic']['us-phonetic'] + ']'
                elif 'uk-phonetic' in j['basic'].keys():
                    print '[' + j['basic']['uk-phonetic'] + ']'
                elif 'phonetic' in j['basic'].keys():
                    print '[' + j['basic']['phonetic'] + ']'

                if 'explains' in j['basic'].keys():
                    for each in j['basic']['explains']:
                        print each
                    
            print
            if 'web' in j.keys():
                for each in j['web']:
                    print each['key']
                    for v in each['value']:
                        print '    ' + v
                    print
                        
                    
def main():
    dict = dictionary()
    if len(sys.argv) == 1:
        while 1:
            query = raw_input('> ').strip()
            if query in ['q()', 'quit()', 'exit()']:
                exit(0)
            else:
                dict.translate(query)
    else:
        query = ' '.join(sys.argv[1:])
        dict.translate(query)

if __name__ == '__main__':
    main()
