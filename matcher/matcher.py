# -*- coding: utf-8 -*-
import requests
from pypinyin import lazy_pinyin

def getAssociativeWords(word):
    host = 'http://sug.so.360.cn/suggest/word'
    payload = {
        'format': 'json',
        'encodein': 'utf-8',
        'encodeout': 'utf-8',
        'word': word
    }

    headers = {
        'Referer': 'http://www.so.com/',
        'User-Agent': 'sMozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17'
    }

    r = requests.get(host, params=payload, headers=headers)
    j = r.json()
    return [each['word'] for each in j['result']]


def getPossiblePinYinList(phrase):
    if not isinstance(phrase, unicode):
        try:
            phrase = phrase.decode('utf-8')
        except:
            pass

    words = [each for each in phrase]
    spy = ''.join(lazy_pinyin(words[0]))
    fpy = ''.join(lazy_pinyin(words[1:]))
    return [''.join([spy, fpy]), ''.join([fpy, spy])]
    

def pinyinMatchWords(p):
    pass


def main():
    pass



def calc_weight(nameList):
    N = len(nameList)
    wordList = []
    wordDict = {}
    
    for name in nameList:
        pattern = re.compile(r'[a-zA-Z0-9\s\t\n]+')
        name = re.sub(pattern, '', name).replace('\xc2\xb7', '')    #delete dot

        tempList = split_into_words(name)

        for word in tempList:
            if word not in wordList:
                wordList.append(word)
                wordDict[word] = {}
    
    for word in wordList:
        n = 0
        for name in nameList:
            if word in name:
                n += 1
        wordDict[word] = np.log(N / float(n))

    return wordDict



def SC(A, B, w):
    M = len(A)
    N = len(B)
    m = M/3
    n = N/3
        
    if m == 0 or n == 0:
        return 0

    a = []
    b = []
    i = 0
    while i < M:
        a.append(A[i:i+3])
        i += 3
    i = 0
    while i < N:
        b.append(B[i:i+3])
        i += 3

    SC = 0.0
    for i in range(m):
        C = []
        for k in range(n):
            if a[i] == b[k]:
                C.append(k)

        d = n
        if C != []:
            d = min(abs(each - i) for each in C)

        CC = float(n - d)/float(n) * w[a[i]]
        SC += CC
    
    SC /= float(m)

    return SC


def similarity(A, B, wA, wB):
    return (SC(A, B, wA) + SC(B, A, wB))/2.0




if __name__ == '__main__':
    '''
    l = getAssociativeWords('python')
    for each in l:
        print each
    '''
    main()
