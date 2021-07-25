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
        lis = await parser.get_films(1)
        return render_template('index.html', lis=lis)
    except Exception as e:
        return {"error" : 1, "message" : str(e)}, 400

if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0")
