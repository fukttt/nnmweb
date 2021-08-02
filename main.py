from pars import *
from flask import Flask, request, render_template, redirect, url_for
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
parser = Parser()

@app.route("/")
async def index():
    try:
        page = request.args.get('page', default = 1, type = int)
        lis = await parser.get_films(page, 10)
        return render_template('index.html', lis=lis, page=page)
    except Exception as e:
        return {"error" : 1, "message" : str(e)}, 400

@app.route("/soft")
async def soft():
    try:
        page = request.args.get('page', default = 1, type = int)
        lis = await parser.get_films(page, 19)
        return render_template('index.html', lis=lis, page=page)
    except Exception as e:
        return {"error" : 1, "message" : str(e)}, 400
@app.route("/games")
async def games():
    try:
        page = request.args.get('page', default = 1, type = int)
        lis = await parser.get_films(page, 9)
        return render_template('index.html', lis=lis, page=page)
    except Exception as e:
        return {"error" : 1, "message" : str(e)}, 400
@app.route("/search", methods=['GET', 'POST'])
async def search():
    try:
        search = request.form.get('search')
        lis = await parser.get_search(search)
        return render_template('search.html', lis=lis)
    except Exception as e:
        return {"error" : 1, "message" : str(e)}, 400

if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0")
