from pars import *
from flask import Flask, request, render_template, redirect, url_for
from flask_cors import CORS
import configparser
from utils import torrent
import json

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
parser = Parser()
torrentList = []
config = configparser.ConfigParser()
config.read("settings.ini")

@app.route("/")
async def index():
    try:
        page = request.args.get('page', default = 1, type = int)
        lis = await parser.get_films(page, 10)
        return render_template('index.html', lis=lis, page=page, torCount=str(len(torrentList)))
    except Exception as e:
        return {"error" : 1, "message" : str(e)}, 400

@app.route("/soft")
async def soft():
    try:
        page = request.args.get('page', default = 1, type = int)
        lis = await parser.get_films(page, 19)
        return render_template('index.html', lis=lis, page=page, torCount=str(len(torrentList)))
    except Exception as e:
        return {"error" : 1, "message" : str(e)}, 400
@app.route("/games")
async def games():
    try:
        page = request.args.get('page', default = 1, type = int)
        lis = await parser.get_films(page, 9)
        return render_template('index.html', lis=lis, page=page, torCount=str(len(torrentList)))
    except Exception as e:
        return {"error" : 1, "message" : str(e)}, 400
# search page didnt working. Seems like it will be too long for getting 50 magnet links
@app.route("/search", methods=['GET', 'POST'])
async def search():
    try:
        search = request.form.get('search')
        lis = await parser.get_search(search)
        return render_template('search.html', lis=lis)
    except Exception as e:
        return {"error" : 1, "message" : str(e)}, 400
@app.route("/newTorrent", methods=['POST'])
async def newTorrent():
    try:
        req = request.get_json()
        newtor = torrent.TorrentNode(req['magnet'], config['DEFAULT']['downloadpath'])
        newtor.start()
        print ("New torrent file started downloading")
        torrentList.append(newtor)
        return {"error": 0, "message": "Created succesfully."}, 200
    except Exception as e:
        return {"error" : 1, "message" : str(e)}, 400
@app.route("/getTorrentList", methods=['GET'])
async def getTorrentList():
    try:
        list = []
        for tor in torrentList:
            list.append(tor.status +":"+ str(round(tor.downspeed)) + "KB/S" + ":" + str(round(tor.progress))  + ":" + str(tor.name))
        return json.dumps(list), 200
    except Exception as e:
        return {"error" : 1, "message" : str(e)}, 400


@app.route("/settings")
async def settings():
    try:
        return render_template('settings.html', path=config['DEFAULT']['downloadpath'], torCount=str(len(torrentList)))
    except Exception as e:
        return {"error": 1, "message": str(e)}, 400

@app.route("/setPath", methods=['POST'])
async def setPath():
    try:
        req = request.get_json()
        config['DEFAULT']['downloadpath'] = req['path']
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)
        return {"error": 0, "message": "Changed succesfully."}, 200
    except Exception as e:
        return {"error" : 1, "message" : str(e)}, 400

if __name__=="__main__":

    app.run(debug=True, host="0.0.0.0")
