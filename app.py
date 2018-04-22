from flask import Flask, render_template, request, redirect, Response, make_response, jsonify
import cv2
import numpy as np
import base64
import gps
from random import *


app = Flask(__name__)

@app.route('/')
def output():

    # serve index template
    return render_template('index.html', url = "api/google")

@app.route('/api/google')
def random_number():
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)

if __name__ == '__main__':
    # run!
    gps.__init__('practice.json')
    print(gps.getBikeDistance())
    app.run()
