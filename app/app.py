from flask import Flask, render_template

app = Flask(__name__)


# home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/submit')
def submit():
    return render_template('submit.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
