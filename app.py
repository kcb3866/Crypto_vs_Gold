from flask import Flask, render_template, redirect
import requests
import json
from config import API_KEY, CRYPTO_ROUTE, GOLD_ROUTE



app = Flask(__name__)

@app.route("/")
def index():
    crypto_request = requests.get(f'{CRYPTO_ROUTE}{API_KEY}') #API CALL
    gold_request = requests.get(f'{GOLD_ROUTE}{API_KEY}') #API CALL
    crypto = json.loads(crypto_request)
    gold = json.loads(gold_request)
    return render_template("index.html", crypto=crypto, gold=gold)


@app.route("/api_call")
def caller(): 
    crypto = []
    gold = []
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
