# Aplicacion para inversiones en cryptomonedas, hecha con Flask con SQLite y JS

Programa hecho en python con el framework Flask y SQLite, JS para validar html

# Instalacion
- Crear entorno en python y ejecutar el comando
```
pip install -r requirements.txt
```
La libreria utilizada en flask https://flask-wtf.readthedocs.io/en/1.2.x/

# Config
Renombrar el archivo config_template.py a config.py y agregar la siguiente linea:
``` ORIGIN_DATA = "data/db_inversiones.sqlite" ```

# Ejecucion del programa
Inicializar parametros para servidor (se hace por la terminal)
En windows:   
``` set FLASK_APP=main.py ```

En mac:
``` export FLASK_APP=main.py ```


# Comando para ejecutar el servidor:   
``` flask --app main run ```

# Comando para ejecutar el servidor en modo debug y ejecutar cambios en tiempo real
``` flask --app main --debug run ```


# Otra opcion de ejecucion: 
Crear un archivo .env y dentro agregar lo siguiente:

``` FLASK_APP=main.py ```
``` FLASK_DEBUG=True ```

Luego se puede ejecutar por consola con solo:

``` flask run ```


Todo se ejecuta en el servidor web propio del sistema operativo, en un puerto especifico:  * Running on http://127.0.0.1:5000    esto es lo mismo que http://localhost:5000

A veces este puerto esta ocupado por otro programa. 
Para ejecutarlo en otro puerto hay que usar otro comando: 
``` flask --app main run -p 5002 ```   

Si se cambia hay que cambiarlo en las url para ejecutar las funciones


