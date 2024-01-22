from app_inversiones import app
from app_inversiones.models import *
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
    

@app.route(f"/api/{VERSION}/tasa/<moneda_from>/<moneda_to>")
def get_tasa(moneda_from, moneda_to):
    pass