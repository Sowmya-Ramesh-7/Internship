from flask import Flask
app = Flask(__name__) # Create an instance of a Flask Application
# @app.route("/") # Application Routing
# def hello_world():
#     return "<p>Hello, World!</p>"

@app.route("/", methods=["GET"])
def hello_get():
    return "<p>Hello, GET!</p>"

@app.route("/", methods=["POST"])
def hello_post():
    return "<p>Hello, POST!</p>"

@app.route("/", methods=["PUT"])
def hello_put():
    return "<p>Hello, PUT!</p>"

@app.route("/", methods=["PATCH"])
def hello_patch():
    return "<p>Hello, PATCH!</p>"

@app.route("/", methods=["DELETE"])
def hello_delete():
    return "<p>Hello, Delete!</p>"