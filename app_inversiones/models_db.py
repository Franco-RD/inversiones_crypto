from app_inversiones.conexion import Conexion
from app_inversiones.models_api import get_neto_valor_actual


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
    if crypto_from != 'EUR':
        conectarSaldoTo = Conexion(f"SELECT SUM(cantidad_to) FROM investments WHERE moneda_to = '{crypto_from}';")
        saldo_to = conectarSaldoTo.res.fetchone()
        conectarSaldoTo.con.close()

        conectarSaldoFrom = Conexion(f"SELECT SUM(cantidad_from) FROM investments WHERE moneda_from = '{crypto_from}';")
        saldo_from = conectarSaldoFrom.res.fetchone()
        conectarSaldoFrom.con.close()

        saldo = saldo_to[0] - saldo_from[0]

        if float(saldo) >= float(quantity_from):  #Hay que ponerles float, sobre todo porque el quantity_from llega como str
            return True
        else:
            return False
    
    else:
        return True
    

def get_valor_actual():
    #Toma todos los valores unicos de moneda_to de la db
    conectarMonedaTo = Conexion("SELECT DISTINCT moneda_to FROM investments;")
    monedas_to = conectarMonedaTo.res.fetchall()  # [('BTC',), ('ETH',), ('EUR',), ('SOL',), ('ADA',)]
    conectarMonedaTo.con.close()

    #Guarda la cantidad total de cada moneda de moneda_to en el dic crypto_quantity como par 'moneda': cantidad total
    crypto_quantity = {}
    for moneda in monedas_to:  #moneda = tupla ('BTC',)     
        if moneda[0] != 'EUR':  
            conectarMonedasToQuantity = Conexion(f"SELECT SUM(cantidad_to) FROM investments WHERE moneda_to = '{str(moneda[0])}';")
            crypto_quantity[moneda[0]] = conectarMonedasToQuantity.res.fetchone()[0]
            conectarMonedasToQuantity.con.close()


    #Toma todos los valores unicos de moneda_from de la db
    conectarMonedaFrom = Conexion("SELECT DISTINCT moneda_from FROM investments;")
    monedas_from = conectarMonedaFrom.res.fetchall()  
    conectarMonedaFrom.con.close()

    #Resta la cantidad total (suma de cantidades de cantidad_from) de cada moneda del diccionario para que en el diccionario queden las cantidades netas
    for moneda in monedas_from: #moneda = tupla ('BTC',) 
        if moneda[0] != 'EUR':
            for item in crypto_quantity:
                if item == moneda[0]: 
                    conectarMonedasFromQuantity = Conexion(f"SELECT SUM(cantidad_from) FROM investments WHERE moneda_from = '{str(moneda[0])}';")
                    crypto_quantity[item] -= conectarMonedasFromQuantity.res.fetchone()[0]
                    conectarMonedasFromQuantity.con.close()

    return crypto_quantity  #{'BTC': 5.0046, 'ETH': -3.551, 'SOL': 253.2116, 'ADA': 3366.9327}


def get_status():
    #Obtiene la suma de la columna cantidad_from donde moneda_from es EUR
    conectarInvertido = Conexion("SELECT SUM(cantidad_from) FROM investments WHERE moneda_from = 'EUR';")
    invertido = conectarInvertido.res.fetchone()
    conectarInvertido.con.close()

    #Obtiene la suma de la columna cantidad_to donde moneda_to es EUR
    conectarRecuperado = Conexion("SELECT SUM(cantidad_to) FROM investments WHERE moneda_to = 'EUR';")
    recuperado = conectarRecuperado.res.fetchone()
    conectarRecuperado.con.close()

    valor_compra = float(invertido[0]) - float(recuperado[0])

    #Obtiene el saldo neto de cada cryptomoneda, lo pasa a EUR y acumula para conseguir el valor_actual
    netos_crypto = get_valor_actual()  #{'BTC': 5.0046, 'ETH': -3.551, 'SOL': 253.2116, 'ADA': 3366.9327}
    valor_actual = 0
    for item in netos_crypto:
        valor_actual += get_neto_valor_actual(item, netos_crypto[item])
        print(valor_actual)

    return {"invertido": invertido[0], "recuperado": recuperado[0], "valor_compra": valor_compra, "valor_actual": valor_actual}

    