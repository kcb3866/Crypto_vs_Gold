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

# create route that renders index.html template
@app.route("/")
def home():

    return render_template("index.html")


@app.route("/api/btc")
def btc_pred():

    result = [{
        "y_pred": y_pred.squeeze().values.tolist(),
        "y_test": y_test.squeeze().values.tolist(),
    }]

    return jsonify(result)


if __name__ == "__main__":
    app.run()
