from app_inversiones import app
from app_inversiones.models_db import *
from app_inversiones.models_api import *
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
def tasa_conversion(moneda_from, moneda_to):
    data = get_exchange_rate(moneda_from=moneda_from, moneda_to=moneda_to) 

    try:
        return jsonify(
            {
                "rate": data['rate'], 
                "time": data['time'],
                "monedas": {"from": moneda_from, "to": moneda_to},
                "status": "Success"
            }
        ), HTTPStatus.OK
        
    except Exception as e:
        return jsonify(
            {
                "error": data['error'],                 
                "status": "Error"
            }
        ), HTTPStatus.BAD_REQUEST
        

@app.route(f"/api/{VERSION}/movimiento", methods=["POST"])
def insert_movement():
    datos = request.json
  
    try:
        insert([datos['date'], datos['time'], datos['moneda_from'], datos['quantity_from'], datos['moneda_to'], datos['quantity_to']])
        id = get_last_id(datos['date'], datos['time'])
        haySaldo = get_saldo_crypto(datos['moneda_from'], datos['quantity_from'])

        if haySaldo:
            return jsonify(
                {
                    "id": id,            
                    "monedas": {"from": datos['moneda_from'], "to": datos['moneda_to']},
                    "status": "Success"
                }
            ), HTTPStatus.CREATED
        
        else:
            return jsonify(
                {            
                    "mensaje": "No hay saldo suficiente",
                    "status": "Fail"
                }
            ), HTTPStatus.OK
    
    except sqlite3.Error as e:
        return jsonify(
            {
                "data": str(e),
                "status": "Error"
            }
        ), HTTPStatus.BAD_REQUEST
