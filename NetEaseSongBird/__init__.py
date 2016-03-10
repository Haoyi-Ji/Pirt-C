# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, url_for, redirect
from SongDownloader import SongDownloader
app  = Flask(__name__)
app.secret_key = 'Hidden Markov'
sd = SongDownloader()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        return redirect(url_for('search', query=request.form['query']))

    return render_template('main.html')


@app.route('/song/<songid>', methods=['GET', 'POST'])
def song(songid):
    if request.method == 'POST':
        return redirect(url_for('search', query=request.form['query']))

    songdata = sd.getSongData(songid)

    return render_template('song.html', songdata=songdata)


@app.route('/artist/<artistid>/', methods=['GET', 'POST'])
def artist(artistid):
    if request.method == 'POST':
        return redirect(url_for('search', query=request.form['query']))

    artistdata = sd.getArtistDetail(artistid)

    return render_template('artist.html', artistdata=artistdata)


@app.route('/album/<albumid>', methods=['GET', 'POST'])
def album(albumid):
    if request.method == 'POST':
        return redirect(url_for('search', query=request.form['query']))

    albumdata = sd.getAlbumDetail(albumid)

    return render_template('album.html', albumdata=albumdata)


@app.route('/search/<query>/', methods=['GET', 'POST'])
def search(query):
    if request.method == 'POST':
        return redirect(url_for('search', query=request.form['query']))

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
