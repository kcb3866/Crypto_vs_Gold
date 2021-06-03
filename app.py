from flask import Flask, render_template, redirect
import requests
import json
import pandas as pd
import plotly
import plotly.express as px
from config import API_KEY, CRYPTO_ROUTE, GOLD_ROUTE
from tensorflow.keras.models import load_model

def ML_Forecast(crypto=None,gold=None): #Machine Learning Model Here
    model = load_model("crypto_gold_price_forecasting.h5")
    pass


app = Flask(__name__)

@app.route("/")
def index():
    crypto_request = requests.get(f'{CRYPTO_ROUTE}{API_KEY}') #API CALL
    gold_request = requests.get(f'{GOLD_ROUTE}{API_KEY}') #API CALL
    crypto_list = json.loads(crypto_request)
    gold_list = json.loads(gold_request)
    crypto,gold = ML_Forecast(crypto_list), ML_Forecast(gold_list)
    df = pd.DataFrame({
        "Crypto": crypto,
        "Gold": gold})
    fig = px.line(df, x=df["Datetime"], y=df["Crypto Price", "Gold Price"])
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('templates/index.html', graphJSON=graphJSON)


if __name__ == "__main__":
    app.run(debug=True)


def notdash():

