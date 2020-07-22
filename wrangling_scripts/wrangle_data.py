#!/usr/bin/env python
# coding: utf-8

import requests
import pandas as pd
import plotly.graph_objects as go
# from apscheduler.schedulers.blocking import BlockingScheduler

# define scheduler
# sched = BlockingScheduler()

# data is retrieved and coverted to pd dfs

# @sched.scheduled_job('interval', hours=2)
def get_data():

    confirmed = 'https://raw.githubusercontent.com/dsfsi/covid19za/master/data/covid19za_provincial_cumulative_timeline_confirmed.csv'
    recoveries = 'https://raw.githubusercontent.com/dsfsi/covid19za/master/data/covid19za_provincial_cumulative_timeline_recoveries.csv'
    deaths = 'https://raw.githubusercontent.com/dsfsi/covid19za/master/data/covid19za_provincial_cumulative_timeline_deaths.csv'
    testing = 'https://raw.githubusercontent.com/dsfsi/covid19za/master/data/covid19za_provincial_cumulative_timeline_testing.csv'

    confirmed_df = pd.read_csv(confirmed)
    recoveries_df = pd.read_csv(recoveries)
    deaths_df = pd.read_csv(deaths)
    testing_df = pd.read_csv(testing)

    confirmed_df['date'] = pd.to_datetime(confirmed_df['date'], dayfirst=True)
    recoveries_df['date'] = pd.to_datetime(recoveries_df['date'], dayfirst=True)
    deaths_df['date'] = pd.to_datetime(deaths_df['date'], dayfirst=True)
    testing_df['date'] = pd.to_datetime(testing_df['date'], dayfirst=True)

    confirmed_df = confirmed_df[['date', 'EC', 'FS', 'GP', 'KZN', 'LP', 'MP', 'NC', 'NW', 'WC', 'UNKNOWN']]
    recoveries_df = recoveries_df[['date', 'EC', 'FS', 'GP', 'KZN', 'LP', 'MP', 'NC', 'NW', 'WC', 'UNKNOWN']]
    deaths_df = deaths_df[['date', 'EC', 'FS', 'GP', 'KZN', 'LP', 'MP', 'NC', 'NW', 'WC', 'UNKNOWN']]
    testing_df = testing_df[['date', 'EC', 'FS', 'GP', 'KZN', 'LP', 'MP', 'NC', 'NW', 'WC', 'UNKNOWN']]

    confirmed_df['total'] = confirmed_df[['EC', 'FS', 'GP', 'KZN', 'LP', 'MP', 'NC', 'NW', 'WC', 'UNKNOWN']].sum(axis=1)
    recoveries_df['total'] = recoveries_df[['EC', 'FS', 'GP', 'KZN', 'LP', 'MP', 'NC', 'NW', 'WC', 'UNKNOWN']].sum(axis=1)
    deaths_df['total'] = deaths_df[['EC', 'FS', 'GP', 'KZN', 'LP', 'MP', 'NC', 'NW', 'WC', 'UNKNOWN']].sum(axis=1)
    testing_df['total'] = testing_df[['EC', 'FS', 'GP', 'KZN', 'LP', 'MP', 'NC', 'NW', 'WC', 'UNKNOWN']].sum(axis=1)

    return confirmed_df, recoveries_df, deaths_df

confirmed_df, recoveries_df, deaths_df = get_data()

# chart functions defined to convert dfs

# @sched.scheduled_job('interval', hours=2)
def get_main_chart(province='total', confirmed_df=confirmed_df,
                    recoveries_df=recoveries_df, deaths_df=deaths_df):

    '''
    Creates data (namely figures) used for Plotly area charts given province name

    INPUT: optional province column name in string format
    OUTPUT: data in list form and layout dict

    '''

    confirmed_df = confirmed_df[['date', province]]
    recoveries_df = recoveries_df[['date', province]]
    deaths_df = deaths_df[['date', province]]

    if province == 'total':
        province_name = 'South Africa'
    else:
        province_name = province

    layout = dict(title = "Confirmed COVID-19 related cases (" + str(province_name) + ")",
                xaxis = dict(title = 'Date'),
                yaxis = dict(title = 'Confirmed'))

    data = []

    data.append(go.Scatter(x=confirmed_df['date'], y=confirmed_df[province],
                             fill='tozeroy',
                             fillcolor = 'rgba(211,47,47,0.7)',
                             mode='none',
                             name='Contracted'))

    data.append(go.Scatter(x=recoveries_df['date'], y=recoveries_df[province],
                             fill='tozeroy',
                             fillcolor = 'rgba(0,188,212,0.7)',
                             mode='none',
                             name='Recovered'))

    data.append(go.Scatter(x=deaths_df['date'], y=deaths_df[province],
                             fill='tozeroy',
                             fillcolor = 'rgba(97,97,97,1)',
                             mode='none',
                             name='Deaths'))

    fig = go.Figure()

    fig.update_layout(layout)

    for i in data:
        fig.add_trace(i)

    return data, layout

# @sched.scheduled_job('interval', hours=2)
def get_ratio_chart(province='total', confirmed_df=confirmed_df,
                    recoveries_df=recoveries_df, deaths_df=deaths_df):

    '''
    Creates data (namely figures) used for Plotly ratio area charts given province name

    INPUT: optional province column name in string format
    OUTPUT: data in list form and layout dict

    '''


    ratio_df = pd.merge(confirmed_df[['date', province]], recoveries_df[['date', province]], on='date')
    ratio_df.columns = ['date', 'confirmed', 'recovered']

    ratio_df['ratio'] = ratio_df['confirmed'] - ratio_df['recovered']

    if province == 'total':
        province_name = 'South Africa'
    else:
        province_name = province

    layout = dict(title = "Confirmed cases excluding recoveries (" + str(province_name) + ")",
            xaxis = dict(title = 'Date'),
            yaxis = dict(title = 'Confirmed'))

    data = go.Scatter(x=ratio_df['date'], y=ratio_df['ratio'],
                             fill='tozeroy',
                             fillcolor = 'rgba(230,74,25,0.7)',
                             mode='none',
                             name='Contracted')

    return [data], layout

provinces = ['EC', 'FS', 'GP', 'KZN', 'LP', 'MP', 'NC', 'NW', 'WC']
provinces.append('total')

figures = []

# @sched.scheduled_job('interval', hours=2)
def get_slider_chart(confirmed_df=confirmed_df):

    '''
    Creates data (namely figures) used for Plotly slider chart

    INPUT: optional province column name in string format
    OUTPUT: figures list which includes data in list form and layout dict

    '''

    layout = dict(title = "Confirmed COVID-19 related cases by province",
                xaxis = dict(title = 'Date', rangeslider=dict(visible=True)),
                yaxis = dict(title = 'Confirmed'))

    data = []


    data.append(go.Scatter(x=confirmed_df['date'], y=confirmed_df['GP'],
                             mode='lines',
                             line = dict(color='#EF476F', width=2),
                             name='GP'))

    data.append(go.Scatter(x=recoveries_df['date'], y=recoveries_df['WC'],
                             mode='lines',
                             line = dict(color='#FFD166', width=2),
                             name='WC'))

    data.append(go.Scatter(x=deaths_df['date'], y=deaths_df['EC'],
                             mode='lines',
                             line = dict(color='#06D6A0', width=2),
                             name='EC'))

    data.append(go.Scatter(x=deaths_df['date'], y=deaths_df['FS'],
                             mode='lines',
                             line = dict(color='#118AB2', width=2),
                             name='FS'))

    data.append(go.Scatter(x=confirmed_df['date'], y=confirmed_df['KZN'],
                             mode='lines',
                             line = dict(color='#073B4C', width=2),
                             name='KZN'))

    data.append(go.Scatter(x=recoveries_df['date'], y=recoveries_df['LP'],
                             mode='lines',
                             line = dict(color='#3F84E5', width=2),
                             name='LP'))

    data.append(go.Scatter(x=deaths_df['date'], y=deaths_df['MP'],
                             mode='lines',
                             line = dict(color='#C17817', width=2),
                             name='MP'))

    data.append(go.Scatter(x=deaths_df['date'], y=deaths_df['NC'],
                             mode='lines',
                             line = dict(color='#3F784C', width=2),
                             name='NC'))

    data.append(go.Scatter(x=deaths_df['date'], y=deaths_df['NW'],
                             mode='lines',
                             line = dict(color='#F0E2E7', width=2),
                             name='NW'))

    fig = go.Figure()

    fig.update_layout(layout)

    fig.update_xaxes(rangeslider_visible=True)

    for i in data:
        fig.add_trace(i)

    figures.append(dict(data=data, layout=layout))

    return figures

# @sched.scheduled_job('interval', hours=2)
def get_all_main_charts():

    '''
    Returns list of Plotly area chart data and layout in list form

    INPUT: None
    OUTPUT: figures list consisting of dict(data=data, layout=layout)

    '''

    for prov in provinces:
        data, layout = get_main_chart(prov)
        figures.append(dict(data=data, layout=layout))

    return figures

# @sched.scheduled_job('interval', hours=2)
def get_all_ratio_charts():

    '''
    Returns list of Plotly area ratio chart data and layout in list form

    INPUT: None
    OUTPUT: figures list consisting of dict(data=data, layout=layout)

    '''

    for prov in provinces:
        data, layout = get_ratio_chart(prov)
        figures.append(dict(data=data, layout=layout))

    return figures

# sched.start()
