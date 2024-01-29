from app_inversiones.conexion import Conexion

def select_all():
    conectar = Conexion("SELECT * FROM investments;")
    filas = conectar.res.fetchall()  #res.fetchall() si trae los datos de las columnas nada mas en un a lista de tuplas (1, 2024-01-01, Nomina Enero, 1500)
    columnas = conectar.res.description  #Nombres de columnas en lista de tuplas  (id,0000) (date,0000) (concept,0000) (quantity,0000)

    lista_diccionario = []
    
    for f in filas:
        posicion = 0
        diccionario = {}
        for c in columnas:
            diccionario[c[0]] = f[posicion]  # c es cada tupla de (nombre columna, 0000), la posicion 0 es el nombre de la columna. f es una tupla con todos los datos de una fila, por eso va cambiando con posicion. 
            posicion += 1                    # En cada iteracion de este for agrega al diccionario el nombre de la columna como clave y el valor de f[posicion]. 
                                             # Cuando termina este for de agregar todos los datos de una fila al diccionario, lo agrega a la lista de diccionarios y pasa a la siguiente fila.
        lista_diccionario.append(diccionario)

    conectar.con.close()
    return lista_diccionario  


def insert(registroMovimiento):
    conectarInsert = Conexion("INSERT into investments (date, time, moneda_from, cantidad_from, moneda_to, cantidad_to) VALUES (?, ?, ?, ?, ?, ?);", registroMovimiento)
    conectarInsert.con.commit()
    conectarInsert.con.close()
    

def get_last_id(registroFecha, registroHora):
    conectarId = Conexion(f"SELECT id FROM investments WHERE date = '{str(registroFecha)}' and time = '{str(registroHora)}';")
    id = conectarId.res.fetchone()
    conectarId.res.close()    
    return id[0]


def get_saldo_crypto(crypto_from, quantity_from):
    conectarSaldoTo = Conexion(f"SELECT SUM(cantidad_to) FROM investments WHERE moneda_to = '{crypto_from}';")
    saldo_to = conectarSaldoTo.res.fetchone()
    conectarSaldoTo.con.close()

    conectarSaldoFrom = Conexion(f"SELECT SUM(cantidad_from) FROM investments WHERE moneda_from = '{crypto_from}';")
    saldo_from = conectarSaldoFrom.res.fetchone()
    conectarSaldoFrom.con.close()

    saldo = saldo_to[0] - saldo_from[0]

    if saldo >= quantity_from:
        return True
    else:
        return False