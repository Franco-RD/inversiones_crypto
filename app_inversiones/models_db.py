from app_inversiones.conexion import Conexion
from app_inversiones.models_api import get_neto_valor_actual

conectar_db = Conexion()

def select_all():
    filas = conectar_db.select_all()[0]  #res.fetchall() si trae los datos de las columnas nada mas en un a lista de tuplas (1, 2024-01-01, Nomina Enero, 1500)
    columnas = conectar_db.select_all()[1]  #Nombres de columnas en lista de tuplas  (id,0000) (date,0000) (concept,0000) (quantity,0000)

    lista_diccionario = []
    
    for f in filas:
        posicion = 0
        diccionario = {}
        for c in columnas:
            diccionario[c[0]] = f[posicion]  # c es cada tupla de (nombre columna, 0000), la posicion 0 es el nombre de la columna. f es una tupla con todos los datos de una fila, por eso va cambiando con posicion. 
            posicion += 1                    # En cada iteracion de este for agrega al diccionario el nombre de la columna como clave y el valor de f[posicion]. 
                                             # Cuando termina este for de agregar todos los datos de una fila al diccionario, lo agrega a la lista de diccionarios y pasa a la siguiente fila.
        lista_diccionario.append(diccionario)

    return lista_diccionario  


def insert(registroMovimiento):
    conectar_db.insert(registroMovimiento)
    

def get_last_id(registroFecha, registroHora):
    id = conectar_db.select_last_id(registroFecha, registroHora)
    return id[0]


def get_saldo_crypto(crypto_from, quantity_from):
    if crypto_from != 'EUR':
        saldo_to = conectar_db.get_suma_moneda("cantidad_to", "moneda_to", crypto_from)
        saldo_from = conectar_db.get_suma_moneda("cantidad_from", "moneda_from", crypto_from)

        saldo = saldo_to[0] - saldo_from[0]

        if float(saldo) >= float(quantity_from):  #Hay que ponerles float, sobre todo porque el quantity_from llega como str
            return True
        else:
            return False
    
    else:
        return True
    

def get_valor_actual():
    #Toma todos los valores unicos de moneda_to de la db
    monedas_to = conectar_db.monedas_unicas("moneda_to")  # [('BTC',), ('ETH',), ('EUR',), ('SOL',), ('ADA',)]

    #Guarda la cantidad total de cada moneda de moneda_to en el dic crypto_quantity como par 'moneda': cantidad total
    crypto_quantity = {}
    for moneda in monedas_to:  #moneda = tupla ('BTC',)     
        if moneda[0] != 'EUR':  
            crypto_quantity[moneda[0]] = conectar_db.get_suma_moneda("cantidad_to", "moneda_to", str(moneda[0]))[0]


    #Toma todos los valores unicos de moneda_from de la db
    monedas_from = conectar_db.monedas_unicas("moneda_from")  

    #Resta la cantidad total (suma de cantidades de cantidad_from) de cada moneda del diccionario para que en el diccionario queden las cantidades netas
    for moneda in monedas_from: #moneda = tupla ('BTC',) 
        if moneda[0] != 'EUR':
            for item in crypto_quantity:
                if item == moneda[0]: 
                    crypto_quantity[item] -= conectar_db.get_suma_moneda("cantidad_from", "moneda_from", str(moneda[0]))[0]
                    

    return crypto_quantity  #{'BTC': 5.0046, 'ETH': -3.551, 'SOL': 253.2116, 'ADA': 3366.9327}


def get_status():
    #Obtiene la suma de la columna cantidad_from donde moneda_from es EUR
    invertido = conectar_db.get_suma_moneda("cantidad_from", "moneda_from", 'EUR')

    #Obtiene la suma de la columna cantidad_to donde moneda_to es EUR
    recuperado = conectar_db.get_suma_moneda("cantidad_to", "moneda_to", 'EUR')
    
    valor_compra = float(invertido[0]) - float(recuperado[0])

    #Obtiene el saldo neto de cada cryptomoneda, lo pasa a EUR y acumula para conseguir el valor_actual
    netos_crypto = get_valor_actual()  #{'BTC': 5.0046, 'ETH': -3.551, 'SOL': 253.2116, 'ADA': 3366.9327}
    valor_actual = 0
    for item in netos_crypto:
        valor_actual += (netos_crypto[item] * get_neto_valor_actual(item))

    return {"invertido": round(invertido[0], 4), "recuperado": round(recuperado[0], 4), "valor_compra": round(valor_compra, 4), "valor_actual": round(valor_actual, 4)}

    