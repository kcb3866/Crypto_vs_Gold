# import necessary libraries
from models import create_classes
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
# import libraries and read the data
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import yfinance as yf


df = yf.download(tickers='BTC-USD', period = '5y', interval = '1d', rounding= True)


# clean and select data
df=df[['Close']]
df.dropna()




# define explanatory variables
df['S_3'] = df['Close'].shift(1).rolling(window=3).mean() 
df['S_9']= df['Close'].shift(1).rolling(window=9).mean() 
df= df.dropna() 
X = df[['S_3','S_9']] 


# define dependent variable
y = df['Close']


# split the data into train and test 
t=.8 
t = int(t*len(df)) 
# Train dataset 
X_train = X[:t] 
y_train = y[:t]  
# Test dataset 
X_test = X[t:] 
y_test = y[t:]


# create linear regression
linear = LinearRegression().fit(X_train,y_train)

# predict bitcoin prices
y_pred = linear.predict(X_test)  
y_pred = pd.DataFrame(y_pred,index=y_test.index,columns = ['price'])  
y_test=pd.DataFrame(y_test)


# check model accuracy with r2 score
r2_score = (linear.score(X[t:],y[t:])*100)
print(f'The R2 Score is {r2_score}')





#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################

# from flask_sqlalchemy import SQLAlchemy
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite"

# # Remove tracking modifications
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# Pet = create_classes(db)

# create route that renders index.html template
@app.route("/")
def home():

    return render_template("index.html")


# # Query the database and send the jsonified results
# @app.route("/send", methods=["GET", "POST"])
# def send():
#     if request.method == "POST":
#         name = request.form["petName"]
#         lat = request.form["petLat"]
#         lon = request.form["petLon"]

#         pet = Pet(name=name, lat=lat, lon=lon)
#         db.session.add(pet)
#         db.session.commit()
#         return redirect("/", code=302)

#     return render_template("form.html")


@app.route("/api/btc")
def btc_pred():

    result = [{
        "y_pred": y_pred.squeeze().values.tolist(),
        "y_test": y_test.squeeze().values.tolist(),
        # "text": hover_text,
        # "hoverinfo": "text",
        # "marker": {
        #     "size": 50,
        #     "line": {
        #         "color": "rgb(8,8,8)",
        #         "width": 1
            # },
        # }
    }]

    return jsonify(result)


if __name__ == "__main__":
    app.run()
