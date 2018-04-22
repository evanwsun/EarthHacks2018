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
                title='Year Progress'
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
        )

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
        graphs = [
            dict(
                data=[
                    dict(
                        x=obesitySteps['steps_binned'],
                        y=obesitySteps['obesity_mean'],
                        type='bar',
                        marker = dict(
                        color=['rgba(204,204,204,1)',
                               'rgba(204,204,204,1)', 'rgba(222,45,38,0.8)','rgba(204,204,204,1)',
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
                        y=stepsAge['miles'],
                        type='bar',
                        marker=dict(
                        color=['rgba(222,45,38,0.8)','rgba(204,204,204,1)',
                               'rgba(204,204,204,1)', 'rgba(204,204,204,1)',
                               'rgba(204,204,204,1)']),

                    ),
                ],
                layout=dict(
                    title='Average miles walked per month'
                )
            )

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
    statsGraphs = getStatsGraphs()
    return render_template('charts2.html',timestamp = datetime.datetime.today(), graphJSON = statsGraphs[1], ids = statsGraphs[0])

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
    gps.__init__('Location History.json')
    app.run()
