from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly
import plotly.express as px
import uproot
# import redis
import json
app = Flask(__name__)
# cache = redis.Redis(host='redis', port=6379)

@app.route('/data', methods=['POST'])
def get_data():
    slider_values = request.json['slider_values']
    # Process your data here based on slider values
    # For simplicity, let's just square the slider values and return
    result = [x**2 for x in slider_values]
    return jsonify(result)

def get_data():
    data = uproot.open('data/Daten.root')
    print(data.keys())

@app.route('/')
def main():
    # return render_template('index.html')

    fig = px.bar(df, x='bin_center', y='n')   
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)   
    return render_template('page.html', graphJSON=graphJSON)

def calculate_histograms(sliders):
    pass

@app.route('/plot', methods=['POST'])
def get_plot():
    slider_values = request.json['slider_values']
    x = np.arange(1,20,100)
    # Process your data here based on slider values
    # For simplicity, let's just square the slider values and return
    result = sum(s * x for s in sliders)        
    plt.plot(x,result)
    plt.savefig('plot.png')
    plt.clf()
    return 'plot.png'
