from flask import Flask, jsonify, render_template
import pandas as pd
import numpy as np
import json

app = Flask(__name__)

# setup global variable for data
data_df = None

@app.route('/')
def index():
   return render_template('index.html')


@app.route('/get_heatmap_data')
def get_heatmap_data():
    with open('data/saint_saens_1.json', 'r') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/get_barchart_data')
def get_barchart_data():
    pass
    # return jsonify(barchart_data)

# ------------------------------------ #
if __name__ == '__main__':
   app.run(debug=True)
