from flask import Flask, render_template, redirect, request, url_for, json
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import json
import plotly
import plotly.graph_objects as go
import datetime

import pandas as pd
import numpy as np



app = Flask(__name__)
app.static_folder = 'static'
app.config["MONGO_DBNAME"] = "Nigeria_fx_data"
app.config["MONGO_URI"] = "mongodb+srv://stephensanwo:stephensanwo@stephencluster-ifq4j.azure.mongodb.net/Nigeria_fx_data"

mongo = PyMongo(app)
environment = "dev"

@app.route('/')
def index():
    documents = []
    for doc in mongo.db.cbn_predict_30_days.find():
        if doc not in documents:
            documents.append(doc)

    data = pd.DataFrame(documents)
    data.iloc[:, 1:]
    data1 = data.transpose()[1:]
    data1.reset_index(inplace=True)
    data1.columns = data1.iloc[0]
    data2 = data1[1:]
    data2['index'] = pd.to_datetime(
        data2['index'], format="%Y-%m-%dT%H:%M:%SZ")

    df = data2

    graphs = [
        dict(
            data=[
                go.Scatter(x=df['index'], y=df['usd_sell'],
                           name="USD Sell", line_color='#cb4335'),

                go.Scatter(x=df['index'], y=df['usd_buy'],
                           name="USD Buy", line_color='#008080')
            ],
            layout=dict(
                config={'displayModeBar': False},
                template='simple_white',
                font=dict(family="Helvetica",
                          size=12,
                          color="#000000"),
                title='Predicted USD Buy and Sell rates 30 days forward',
                width=360,
                height=500,
                xaxis={
                    "showgrid": False,
                    "rangeslider_visible": True,
                    "fixedrange": True
                },
                yaxis={
                    "type": 'linear',
                    "showgrid": True,
                    "fixedrange": True,
                    # "range": [305, 308]
                },
                autosize=False,
                hovermode="closest",
                legend={
                    "x": -.1,
                    "y": 1.2,
                    "orientation": 'h'
                },
                margin={
                    "b": 52,
                    "l": 20,
                    "r": 20,
                    "t": 150,
                    "pad": 0,
                    "autoexpand": True
                },
                automargin=True,

                titlefont={
                    "family": "Helvetica",
                    "size": 12.0,
                    "color": "#000000"
                },
            )
        ),

        dict(
            data=[
                go.Scatter(x=df['index'], y=df['gbp_sell'],
                           name="GBP Sell", line_color='#cb4335'),

                go.Scatter(x=df['index'], y=df['gbp_buy'],
                           name="GBP Buy", line_color='#008080')
            ],
            layout=dict(
                config={'displayModeBar': False},
                template='simple_white',
                font=dict(family="Helvetica",
                          size=12,
                          color="#000000"),
                title='Predicted GBP Buy and Sell rates 30 days forward',
                width=360,
                height=500,
                xaxis={
                    "showgrid": False,
                    "rangeslider_visible": True,
                    "fixedrange": True
                },
                yaxis={
                    "type": 'linear',
                    "showgrid": True,
                    "fixedrange": True,
                    # "range": [305, 308]
                },
                autosize=False,
                hovermode="closest",
                legend={
                    "x": -.1,
                    "y": 1.2,
                    "orientation": 'h'
                },
                margin={
                    "b": 52,
                    "l": 20,
                    "r": 20,
                    "t": 150,
                    "pad": 0,
                    "autoexpand": True
                },
                automargin=True,

                titlefont={
                    "family": "Helvetica",
                    "size": 12.0,
                    "color": "#000000"
                },
            )
        ),

        dict(
            data=[
                go.Scatter(x=df['index'], y=df['eur_sell'],
                           name="EUR Sell", line_color='#cb4335'),

                go.Scatter(x=df['index'], y=df['eur_buy'],
                           name="EUR BUY", line_color='#008080')
            ],

            layout=dict(
                template='simple_white',
                font=dict(family="Helvetica",
                          size=12,
                          color="#000000"),
                title='Predicted EURO Buy and Sell rates 30 days forward',
                width=360,
                height=500,
                xaxis={
                    "showgrid": False,
                    "rangeslider_visible": True,
                    "fixedrange": True
                },
                yaxis={
                    "type": 'linear',
                    "showgrid": True,
                    "fixedrange": True,
                    # "range": [305, 308]
                },
                autosize=False,
                hovermode="closest",
                legend={
                    "x": -.1,
                    "y": 1.2,
                    "orientation": 'h'
                },
                margin={
                    "b": 52,
                    "l": 20,
                    "r": 20,
                    "t": 150,
                    "pad": 0,
                    "autoexpand": True
                },
                automargin=True,

                titlefont={
                    "family": "Helvetica",
                    "size": 12.0,
                    "color": "#000000"
                },
            ),

        )
    ]

    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',
                           cbn_rates=mongo.db.cbn_rates.find().sort("_id", -1).limit(10),
                           abokifx_rates=mongo.db.abokifx_rates.find().sort("_id", -1).limit(10),
                           fxmallam_rates=mongo.db.fxmallam_rates.find().sort("_id", -1).limit(10),
                           # cbn_pred_rates=mongo.db.cbn_rates.find().limit(1),
                           # bdc_pred_rates=mongo.db.cbn_rates.find().limit(1),
                           data=data, ids=ids,
                           graphJSON=graphJSON
                           )

# Check environment and run app

if environment == "dev":
    if __name__ == '__main__':
        app.run(host='192.168.8.101', port=5000)
else:
    if __name__ == '__main__':
        # Bind to PORT if defined, otherwise default to 5000.
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port)
