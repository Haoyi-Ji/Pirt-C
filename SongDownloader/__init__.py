# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, url_for, redirect

app  = Flask(__name__)
app.secret_key = 'Hidden Markov'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        return redirect(url_for('search', query=request.form['query']))

    return render_template('main.html')


'''
@app.route('/song/<songid>', methods=['GET', 'POST'])
def song(songid):
    query = request.form['query']
    from SongDownloader import SongDownloader
    sd = SongDownloader()
    searchResult = sd.search(query)

    return render_template('song.html', query=query, searchResult=searchResult)
'''

@app.route('/artist/<artistid>/', methods=['GET', 'POST'])
def artist(artistid):
    if request.method == 'POST':
        return redirect(url_for('search', query=request.form['query']))

    from SongDownloader import SongDownloader
    sd = SongDownloader()
    artistdata = sd.getArtistData(artistid)

    return render_template('artist.html', artistdata=artistdata)


@app.route('/search/<query>/', methods=['GET', 'POST'])
def search(query):
    if request.method == 'POST':
        return redirect(url_for('search', query=request.form['query']))
    
    from SongDownloader import SongDownloader
    sd = SongDownloader()
    searchResult = sd.search(query)

    return render_template('search.html', query=query, searchResult=searchResult)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/login/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/return-file/')
def return_file():
    return send_file('http://yinyueshiting.baidu.com/data2/music/239769084/239769084.mp3?xcode=89640ff9d3a5f5cb48ae5c20176c0886', attachment_filename='music.mp3')



if __name__ == '__main__':
    app.run(debug=True)   
