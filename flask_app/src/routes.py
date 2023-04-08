""" This is the file that implements a flask server to do inferences."""

from __future__ import print_function

import json
import logging

import flask
from flask import request


logging.root.setLevel(logging.INFO)

# The flask app for serving predictions
app = flask.Flask(__name__)


@app.route("/ping", methods=["GET"])
def ping():
    """
    Determine the health of the container by returning a Flask Response object.
    This function returns a Flask Response object with a blank JSON-formatted string and a status of 200, 
    indicating that the container is up and running and ready to accept requests.

    :return: A Flask Response object with an empty JSON-formatted string and a status of 200.
    """
    return flask.Response(response="\n", status=200, mimetype="application/json")


@app.route("/invocations", methods=["POST"])
def predict():
    """
    Perform inference on a single batch of data received in an HTTP request.
    The function decodes the payload of the request, performs the inference using a predictor,
    and returns the prediction as a JSON-formatted response.

    The HTTP request must include a valid CONTENT_TYPE header, which is used to determine the decoding function to use.
    The decoded data is passed to a predictor object, which is responsible for performing the inference.
    The predictor's output is then converted to a JSON format and returned as the HTTP response.

    :return: A Flask Response object containing the prediction results as a JSON-formatted string.
    """
    result = {"message": "Predictions test"}

    return flask.Response(response=result, status=200, mimetype="application/json")


@app.route("/test", methods=["GET"])
def home():
    return json.dumps({"message":"Hi There!"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080')  # Flask startup is required to be placed after route definitions
