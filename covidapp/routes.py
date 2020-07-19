from covidapp import app
import random
import numpy as np
import json, plotly
import plotly.graph_objects as go
from flask import render_template
from wrangling_scripts.wrangle_data import get_all_main_charts, get_all_ratio_charts, get_slider_chart

@app.route('/')
@app.route('/index')

def index():

    figures = get_all_main_charts() + get_all_ratio_charts() + get_slider_chart()

    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',
                           ids=ids,
                           figuresJSON=figuresJSON)
