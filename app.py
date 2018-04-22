from flask import Flask, render_template, request, redirect, Response, make_response, jsonify
import cv2
import numpy as np
import base64
import gps
from random import *
import fastFood
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
import matplotlib.pyplot as plt
import datetime
from io import StringIO, BytesIO
import random

import datetime
app = Flask(__name__)

@app.route('/')
def output():
    fastfreq = fastFood1.getCount('04', '18')
    print(fastfreq)
    totalSpent = fastFood1.getSum('04', '18')
    print (totalSpent)
    aprilWalking = gps.getDistance(1522558800000, "Walk")
    return render_template('charts.html', freq = fastfreq, spent = totalSpent, miles = aprilWalking, timestamp = datetime.datetime.today())


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
    print()
    app.run()
