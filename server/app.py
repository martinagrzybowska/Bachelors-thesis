from flask import Flask, render_template, jsonify

app = Flask(__name__, static_folder = "./dist/static", template_folder = "./dist")

from views import *

app.config.from_pyfile('config.py')

print("Perun GUI is running at http://10.211.55.7:5000/")

if __name__ == "__main__":
    app.run()


