from app_inversiones import app
from app_inversiones.models_db import *
from config import *
from flask import render_template, request, jsonify
from http import HTTPStatus
import sqlite3


@app.route("/")
def index():
    return render_template("index.html")


@app.route(f"/api/{VERSION}/movimientos")
def all_movements():
    try:
        registros = select_all()
        return jsonify(
            {
                "data": registros,
                "status": "Success"
            }
        ), HTTPStatus.OK
    
    except sqlite3.Error as e:
        return jsonify(
            {
                "data": str(e),
                "status": "Fail"
            }
        ), HTTPStatus.BAD_REQUEST
    

@app.route(f"/api/{VERSION}/tasa/<str:moneda_from>/<str:moneda_to>")
def tasa_conversion(moneda_from, moneda_to):
    pass