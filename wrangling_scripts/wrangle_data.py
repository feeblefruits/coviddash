#!/usr/bin/env python
# coding: utf-8

import requests
import pandas as pd

import plotly.graph_objects as go

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

provinces = ['EC', 'FS', 'GP', 'KZN', 'LP', 'MP', 'NC', 'NW', 'WC', 'UNKNOWN']
provinces.append('total')

def get_main_chart(province='total', confirmed_df=confirmed_df,
                    recoveries_df=recoveries_df, deaths_df=deaths_df):

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

    return data

def get_ratio_chart(province='total', confirmed_df=confirmed_df,
                    recoveries_df=recoveries_df, deaths_df=deaths_df):

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

    data = go.Scatter(x=confirmed_df['date'], y=ratio_df['ratio'],
                             fill='tozeroy',
                             fillcolor = 'rgba(230,74,25,0.7)',
                             mode='none',
                             name='Contracted')

    fig = go.Figure()

    fig.update_layout(layout)

    fig.add_trace(data)

    return data

def get_all_main_charts():

    main_charts = []

    for prov in provinces:
        main_charts.append(get_main_chart(prov))

    return main_charts

def get_all_ratio_charts():

    ratio_charts = []

    for prov in provinces:
        ratio_charts.append(get_ratio_chart(prov))

    return ratio_charts
