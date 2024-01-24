from app_inversiones import app
from app_inversiones.models_db import *
from app_inversiones.models_api import *
from config import *
from flask import render_template, request, jsonify
from http import HTTPStatus
import sqlite3
import requests
 

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
def tasa_conversion(moneda_from, moneda_to):
    data = get_exchange_rate(moneda_from=moneda_from, moneda_to=moneda_to) 

    return jsonify(
        {
            "rate": data['rate'], 
            "time": data['time'],
            "monedas": {"from": moneda_from, "to": moneda_to},
            "status": "Success"
        }
    ), HTTPStatus.OK
    