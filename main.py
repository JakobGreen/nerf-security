#!/usr/bin/env python2

""" HTTP Based security system """

from launcher import Launcher2123
from flask import Flask, jsonify, request

APP = Flask(__name__, static_url_path='')

launcher = Launcher2123() 

@APP.route("/")
def status():
    """ Return the current status as JSON """
    return jsonify(result="Some stuff?")

@APP.route("/fire")
def fire():
    failed = False
    try:
        launcher.turretFire()
    except:
        failed = True

    return jsonify(result=(not failed))


APP.run(host='0.0.0.0')
