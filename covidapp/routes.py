from covidapp import app
import json
import plotly
import plotly.graph_objects as go
from flask import render_template
from wrangling_scripts.wrangle_data import get_all_main_charts, get_all_ratio_charts, get_slider_chart
from apscheduler.schedulers.blocking import BlockingScheduler

# define scheduler
sched = BlockingScheduler()

@app.route('/')
@app.route('/index')

# @sched.scheduled_job('interval', hours=2)
def index():

    '''
    INPUT: None
    OUTPUT: updated figures in JSON format for 'index.html' and autoincremented ids

    '''

    fig_1 = get_all_main_charts()
    fig_2 = get_all_ratio_charts()
    fig_3 = get_slider_chart()

    figures = fig_1 + fig_2 + fig_3

    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',
                           ids=ids,
                           figuresJSON=figuresJSON)

# sched.start()
