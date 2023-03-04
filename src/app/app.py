from flask import Flask, jsonify, render_template
import pandas as pd
import numpy as np

app = Flask(__name__)

# setup global variable for data
data_df = None

@app.route('/')
def index():
   return render_template('index.html')


@app.route('/get_piechart_data')
def get_piechart_data():
    pass
    # return jsonify(piechart_data)

@app.route('/get_barchart_data')
def get_barchart_data():
    pass
    # return jsonify(barchart_data)

# ------------------------------------ #
if __name__ == '__main__':
   app.run(debug=True)
