# Aplicacion para inversiones en cryptomonedas, hecha con Flask con SQLite y JS

Programa hecho en python con el framework Flask y SQLite, JS para validar html


# Instalacion
- Crear entorno en python y ejecutar el comando
```
pip install -r requirements.txt
```
La libreria utilizada en flask https://flask-wtf.readthedocs.io/en/1.2.x/


# Config
Renombrar el archivo config_template.py a config.py y agregar la siguientes linea:

``` ORIGIN_DATA = "data/db_inversiones.sqlite" ```

``` VERSION = "version de la app" ```

``` APIKEY = "su api key para apicoins.io" ```

El apikey se puede obtener gratuitamente en la pagina https://docs.coinapi.io/ 
Se debe introducir una direccion de email valida en el campo correspondiente y tocar el boton "GET A FREE API KEY"


# Base de datos
Ya hay una base de datos con su tabla correspondiente vacia creada para poder empezar a utilizar la aplicacion.

De no existir la base de datos, crearla en la carpeta data con el nombre db_inversiones.sqlite
Crearla utilizando el software DB Browser. Descargar la version correspondiente de este link : https://sqlitebrowser.org/dl/

Si no existiese la tabla, o si hay que crear la base de datos desde cero, en "data/create.sql" esta el codigo para crearla.
Una vez creada o abierta la base de datos con DB Browser, crear la tabla  utilzando el codigo de create.sql desde la pestaña "Ejecutar SQL". 


# Ejecucion del programa
Hay un archivo .env con el siguiente codigo:

``` FLASK_APP=main.py ```

``` FLASK_DEBUG=True ```


Lo que permite ejecutar la app por consola con solo:

``` flask run ```

# Otra opcion de ejecucion: 
Si no se quiere usar el archivo .env, se puede inicializar parametros para servidor (se hace por la terminal)
En windows:   
``` set FLASK_APP=main.py ```

En mac:
``` export FLASK_APP=main.py ```



# Comando para ejecutar el servidor:   
``` flask --app main run ```


# Comando para ejecutar el servidor en modo debug y ejecutar cambios en tiempo real
``` flask --app main --debug run ```



Todo se ejecuta en el servidor web propio del sistema operativo, en un puerto especifico:  * Running on http://127.0.0.1:5000    esto es lo mismo que http://localhost:5000

A veces este puerto esta ocupado por otro programa. 
Para ejecutarlo en otro puerto hay que usar otro comando: 
``` flask --app main run -p 5002 ```   

Si se cambia hay que cambiarlo en las url para ejecutar las funciones


