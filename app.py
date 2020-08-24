from flask import Flask, render_template, redirect
import scrape_cars
import pandas as pd
import os
import numpy as np


app = Flask(__name__)

@app.route('/')
def index():
    table_html = ''
    if os.path.isfile('export.csv'):
        df = pd.read_csv('export.csv', index_col= False)
        df.index = np.arange(1, len(df)+1)
        table_html = df.to_html( escape= False)
        table_html = '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous"><div class="table-responsive-sm">' + table_html + '</div>'
    return render_template('index.html', table_html = table_html)

@app.route('/scrape')
def scrape():
    scrape_cars.scrape()

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
