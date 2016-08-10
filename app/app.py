from flask import Flask, request, render_template
from predict.predictor import predict
import numpy as np
from PIL import Image
import json
import re

with open('/home/ubuntu/capstone/app/predict/app_dict.json') as ad:
    app_dict = json.load(ad)

def proc_results(result_list, breed_dict):
    new_list = []
    for tup in result_list:
        breed_idx = str(tup[0])
        breed_name = breed_dict[breed_idx][0]
        breed_desc = breed_dict[breed_idx][1]
        breed_per = tup[1]
        nospace = re.sub('\s*', '', breed_name)
        new_tup = (breed_name, breed_desc, breed_per, nospace)
        new_list.append(new_tup)

    return new_list

app = Flask(__name__)


# home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/submit')
def submit():
    return render_template('submit.html')

@app.route('/classify', methods=['GET', 'POST'])
def classify():
    print 'Reading the img'
    image = Image.open(request.files['imagefile'])
    results = predict(image)
    proc = proc_results(results, app_dict)
    # predictions = predict(imagefile)
    return render_template('result.html', data=proc)

@app.route('/aboutme')
def aboutme():
    return render_template('aboutme.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
