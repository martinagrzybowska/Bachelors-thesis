from flask import Flask, render_template, jsonify

app = Flask(__name__, static_folder = "./dist/static", template_folder = "./dist")

from views import *

app.config.from_pyfile('config.py')

if __name__ == "__main__":
    app.run()


