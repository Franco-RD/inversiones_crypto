import sqlite3
from config import *

class Conexion: 
    def __init__(self):
        self.con = None
        self.cur = None 

    def conectar(self):
        self.con = sqlite3.connect(ORIGIN_DATA)
        self.cur = self.con.cursor()
        
    def select_all(self):
        conexion_select = sqlite3.connect(ORIGIN_DATA)
        cursor_select = conexion_select.cursor()
        res_select = cursor_select.execute("SELECT * FROM investments;")

        rows = res_select.fetchall()
        collumns = res_select.description
        
        conexion_select.close()
        return [rows, collumns]
    
    def insert(self, param = []):
        self.conectar()
        self.res = self.cur.execute("INSERT into investments (date, time, moneda_from, cantidad_from, moneda_to, cantidad_to) VALUES (?, ?, ?, ?, ?, ?);", param)
        self.con.commit()
        self.con.close()

    def select_last_id(self, fecha, hora):
        self.conectar()
        self.res = self.cur.execute(f"SELECT id FROM investments WHERE date = '{str(fecha)}' and time = '{str(hora)}';")
        id = self.res.fetchone() #fetchone da una tupla (id, ####)
        self.con.close()
        return id
    
    def get_suma_moneda(self, columna, moneda_condicion, moneda):
        self.conectar()
        self.res = self.cur.execute(f"SELECT SUM({columna}) FROM investments WHERE {moneda_condicion} = '{moneda}';")
        saldo = self.res.fetchone()
        self.con.close()  
        return saldo
    
    def monedas_unicas(self, moneda):
        self.conectar()
        self.res = self.cur.execute(f"SELECT DISTINCT {moneda} FROM investments;")
        monedas = self.res.fetchall()   # [('BTC',), ('ETH',), ('EUR',), ('SOL',), ('ADA',)]
        self.con.close()
        return monedas