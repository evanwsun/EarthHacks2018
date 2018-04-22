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

app = Flask(__name__)

@app.route('/')
def output():
    return render_template('charts.html', url = "api/google", figure = "fig1.png")

@app.route('/api/google')
def random_number():
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)

@app.route('/fig1.png')
def figure():
    figure = plt.figure()
    figure.axes.append(fastFood1.printSumGraph())
    figure.autofmt_xdate()
    canvas = FigureCanvas(figure)
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
