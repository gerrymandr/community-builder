#!.env/bin/python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the Community Builder API!"

@app.route('project/')

if __name__ == '__main__':
    app.run(debug=True)