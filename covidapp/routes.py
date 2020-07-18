from covidapp import app
import random
import numpy as np
import json, plotly
import plotly.graph_objects as go
from flask import render_template
from wrangling_scripts.wrangle_data import get_main_chart

@app.route('/')
@app.route('/index')

def chart():

    data = get_main_chart('WC')
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',
                            graphJSON=graphJSON)
