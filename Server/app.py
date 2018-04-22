from flask import Flask, render_template, request, redirect, Response, make_response
import colorSegBeta as colorseg
import cv2
import numpy as np
import base64

app = Flask(__name__)

@app.route('/')
def output():

    # serve index template
    return render_template('index.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/ASL_translate', methods=['POST'])
def upload():


if __name__ == '__main__':
    # run!
    app.run()
