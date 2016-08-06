from flask import Flask, render_template

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

@app.route('/aboutme')
def aboutme():
    return render_template('aboutme.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
