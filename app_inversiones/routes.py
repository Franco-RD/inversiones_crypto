from app_inversiones import app
from app_inversiones.models import *
from config import *
from flask import render_template, request, jsonify
from http import HTTPStatus

@app.route("/")
def index():
    return render_template("index.html")