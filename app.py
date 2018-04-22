from flask import Flask, render_template, request, redirect, Response, make_response, jsonify
import numpy as np
import gps2 as gps
import fastFood
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import datetime
from io import StringIO, BytesIO
import plotly
import pandas as pd
import json


import datetime
app = Flask(__name__)

def dashFig():
    base_chart = {
        "values": [40, 15, 15, 15, 15],
        "labels": ["-", "0", "33", "66", "100"],
        "domain": {"x": [0, .48]},
        "marker": {
            "colors": [
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)',
            ],
            "line": {
                "width": 1
            }
        },
        "name": "Gauge",
        "hole": .4,
        "type": "pie",
        "direction": "clockwise",
        "rotation": 108,
        "showlegend": False,
        "hoverinfo": "none",
        "textinfo": "label",
        "textposition": "outside"
    }
    meter_chart = {
        "values": [30, 10, 10, 10],
        "labels": ["Insurance Level", "High", "Medium", "Low"],
        "marker": {
            'colors': [
                'rgb(255, 255, 255)',
                'rgb(255,0,0,)',
                'rgb(255,255,0)',
                'rgb(0,255,0)'
            ]
        },
        "domain": {"x": [0, 0.48]},
        "name": "Gauge",
        "hole": .3,
        "type": "pie",
        "direction": "clockwise",
        "rotation": 90,
        "showlegend": False,
        "textinfo": "label",
        "textposition": "inside",
        "hoverinfo": "none",
        'shapes': [
            {
                'type': 'path',
                'path': 'M 0.235 0.5 L 0.24 0.62 L 0.245 0.5 Z',
                'fillcolor': 'rgba(44, 160, 101, 0.5)',
                'line': {
                    'width': 0.5
                },
                'xref': 'paper',
                'yref': 'paper'
            }
        ]
    }
    layout = {
        'autosize':False,
        'width':150,
        'height':150,
        'margin': {
            'l': 5,
            'r': 5,
            'b': 0,
            't': 5,
            'pad':5
        },
        'xaxis': {
            'showticklabels': False,
            'autotick': False,
            'showgrid': False,
            'zeroline': False,
        },
        'yaxis': {
            'showticklabels': False,
            'autotick': False,
            'showgrid': False,
            'zeroline': False,
        },
        'shapes': [
            {
                'type': 'path',
                'path': 'M 0.235 0.5 L 0.24 0.65 L 0.245 0.5 Z',
                'fillcolor': 'rgba(44, 160, 101, 0.5)',
                'line': {
                    'width': 0.5
                },
                'xref': 'paper',
                'yref': 'paper'
            }
        ],
        'annotations': [
            {
                'xref': 'paper',
                'yref': 'paper',
                'x': 0.23,
                'y': 0.45,
                'text': '12',
                'showarrow': False
            }
        ]
    }

    # we don't want the boundary now
    base_chart['marker']['line']['width'] = 0

    return {"data": [base_chart, meter_chart],
           "layout": layout}



def getFitness():
    rng = pd.date_range('1/1/2011', periods=7500, freq='H')
    ts = pd.Series(np.random.randn(len(rng)), index=rng)
    yearWalking = gps.getYear(1514786400000, "Walk")
    percentages = gps.getPercentages(1514786400000)
    graphs = [
        dict(
            data=[
                dict(
                    x=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                    y=yearWalking,
                    type='Scatter'
                ),
            ],
            layout=dict(
                title='Yearly Active Distance'
            )
        ),

        dict(
            data=[
                {
                    "values": percentages[0:3],
                    "labels":["Walking", "Biking", "Driving"],
                    "hoverinfo": "label+value+percent",
                    "domain": {"x": [0, percentages[-1]]},
                    "type":'pie'
                },
            ],
            layout=dict(
                   title='Method of Transportation, April'
            )
        ),
        dashFig()

    ]

    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    return([ids, graphJSON])


def getStatsGraphs():
        obesitySteps = pd.read_csv('obesity_by_steps_gender.csv')
        obesitySteps = obesitySteps[obesitySteps.gender == "male"]
        stepsAge = pd.read_csv('steps_by_age_gender.csv')
        stepsAge = stepsAge[stepsAge.gender == "male"]
        stepsAge['miles'] = stepsAge['steps_mean']*2.5/5280 * 30

        fastfoodstat = pd.read_csv('fastfood.csv')
        graphs = [
            dict(
                data=[
                    dict(
                        x=obesitySteps['steps_binned'],
                        y=obesitySteps['obesity_mean'],
                        type='bar',
                        marker = dict(
                        color=['rgba(204,204,204,1)',
                               'rgba(204,204,204,1)','rgba(204,204,204,1)',
                               'rgba(204,204,204,1)', 'rgba(222,45,38,0.8)','rgba(204,204,204,1)','rgba(204,204,204,1)',
                               'rgba(204,204,204,1)',
                               'rgba(204,204,204,1)',
                               'rgba(204,204,204,1)']),
                                ),
                ],
                layout=dict(
                    title='Average rate of obesity based on number of steps'
                )
            ),
            dict(
                data=[
                    dict(
                        x=stepsAge['age'],
                        y=stepsAge['steps_mean'],
                        type='bar',
                        marker=dict(
                            color=['rgba(222,45,38,0.8)', 'rgba(204,204,204,1)', 'rgba(204,204,204,1)','rgba(204,204,204,1)','rgba(204,204,204,1)', 'rgba(204,204,204,1)',
                                   'rgba(204,204,204,1)']),

                    ),
                ],
                layout=dict(
                    title='Average Fast Food Frequency'
                )
            ),
            dict(
                data=[
                    dict(
                        x=fastfoodstat['Frequency'],
                        y=fastfoodstat['Obesity Prevalence'],
                        type='bar',
                        marker=dict(
                        color=['rgba(204,204,204,1)','rgba(222,45,38,0.8)','rgba(204,204,204,1)',
                               'rgba(204,204,204,1)']),

                    ),
                ],
                layout=dict(
                    title='Average Fast Food Frequency'
                )
            ),
            dashFig()

        ]

        # Add "ids" to each of the graphs to pass up to the client
        # for templating
        ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]
        # Convert the figures to JSON
        # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
        # objects to their JSON equivalents
        graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
        return ([ids, graphJSON])
@app.route('/')
def output():
    fastfreq = fastFood1.getCount('04', '18')
    print(fastfreq)
    totalSpent = fastFood1.getSum('04', '18')
    print (totalSpent)
    aprilWalking = gps.getDistance(1522558800000, "Walk")
    fitnessStats = getFitness()
    return render_template('charts.html', freq = fastfreq, spent = totalSpent, miles = aprilWalking, timestamp = datetime.datetime.today(), graphJSON = fitnessStats[1], ids = fitnessStats[0])


@app.route('/stats')
def statsOutput():
    fastfreq = fastFood1.getCount('04', '18')
    print(fastfreq)
    totalSpent = fastFood1.getSum('04', '18')
    print (totalSpent)
    aprilWalking = gps.getDistance(1522558800000, "Walk")
    statsGraphs = getStatsGraphs()
    return render_template('charts2.html', freq = fastfreq, spent = totalSpent, miles = aprilWalking, timestamp = datetime.datetime.today(), graphJSON = statsGraphs[1], ids = statsGraphs[0])

@app.route('/FastDollars.png')
def figure():
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    fastFood1.printSumGraph(ax)
    fig.autofmt_xdate()
    canvas = FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    response = make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route('/FastFreq.png')
def figure1():
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    fastFood1.printCountGraph(ax)
    fig.autofmt_xdate()
    canvas = FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    response = make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response


if __name__ == '__main__':
    # run!
    fastFood1 =fastFood.FastFood('transactions(1).csv')
    gps.__init__('practice.json')
    app.run()







