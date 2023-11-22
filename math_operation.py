# Create a Flask microservice to expose mathematical operations. It exposes POST operations for
# the following operations.
# • add -multiply - subtract - divide
import time
import sympy
import sys
import logging
from flask import Flask
from flask import request

sys.set_int_max_str_digits(1000000000)

app = Flask(__name__)
def setup_logger(called):
    def f(*args, **kwargs):
        app.logger.setLevel(logging.INFO)
        request.logger = app.logger
        return called(*args, **kwargs)
    f.__name__ = called.__name__
    return f

def time_request(called):
    def f(*args, **kwargs):
        request.start_time = time.time() * 1000
        res = called(*args, **kwargs)
        request.end_time = time.time() * 1000
        request.time = request.end_time - request.start_time
        app.logger.info('request time: {0}'.format(request.time)) 
        return res
    f.__name__ = called.__name__
    return f

@app.route("/api/add", methods=["POST"])
@time_request
@setup_logger
def add():
    num=request.json
    sum=0
    for i in list(range(10000)):
        sum+=(i+1)
    return "<p>Sum of {0} and {1} is {2}!<br/> sum of 10000 numbers is {0}</p>".format(num['a'],num['b'],(num['a']+num['b']),sum)

@app.route("/api/subtract", methods=["POST"])
def subtract():
    num=request.json
    return "<p>Subtraction of {0} and {1} is {2}!</p>".format(num['a'],num['b'],(num['a']-num['b']))

@app.route("/api/multiply", methods=["POST"])
@time_request
@setup_logger
def multiply():
    n=request.json
    mul=1
    # for i in range(1, n['num'] + 1):
    #     mul *= i
    mul = sympy.Mul(*range(1, n['num'] + 1))
    return "<p>Multiplication of {0}  num is{1}</p>".format(n['num'],str(mul))

@app.route("/api/divide", methods=["POST"])
def divide():
    num=request.json
    return "<p>Division of {0} and {1} is {2}!</p>".format(num['a'],num['b'],(num['a']/num['b']))
