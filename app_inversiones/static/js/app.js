console.log("Funcionando")

let peticion_movimientos = new XMLHttpRequest()  //Creo un objeto de tipo XMLHttpRequest
function peticion_movimientos_handler(){        //Las variables que vamos declarando y usando con this son propias de JS por lo que no hace falta declararlas antes
    if(this.readyState === 4){                       
        if(this.status === 200){            
            const datos = JSON.parse(this.responseText) 
            
            document.getElementById("investments_table").innerHTML="<tr><th>Fecha</th><th>Hora</th><th>From</th><th>Cantidad</th><th>To</th><th>Cantidad</th></tr>" 

            const tabla = document.getElementById("investments_table")  //Variable tabla que representa la tabla en html
            const movimientos = datos.data  //como en routes separamos el JSON con dos claves, data para la info y status para el estado, tenemos que iterar solo sobre data. 

            for (let i = 0; i < movimientos.length; i++) {
                const fila = document.createElement("tr")

                const celda_date = document.createElement("td")
                celda_date.innerHTML = movimientos[i].date
                fila.appendChild(celda_date)

                const celda_time = document.createElement("td")
                celda_time.innerHTML = movimientos[i].time
                fila.appendChild(celda_time)

                const celda_moneda_from = document.createElement("td")
                celda_moneda_from.innerHTML = movimientos[i].moneda_from
                fila.appendChild(celda_moneda_from)

                const celda_cantidad_from = document.createElement("td")
                celda_cantidad_from.innerHTML = movimientos[i].cantidad_from
                fila.appendChild(celda_cantidad_from)

                const celda_moneda_to= document.createElement("td")
                celda_moneda_to.innerHTML = movimientos[i].moneda_to
                fila.appendChild(celda_moneda_to)

                const celda_cantidad_to = document.createElement("td")
                celda_cantidad_to.innerHTML = movimientos[i].cantidad_to
                fila.appendChild(celda_cantidad_to)
                
                tabla.appendChild(fila)                
            }

        }else{
            alert("Aqui se ha producido un error en la consulta")
        }
    }                     
}




window.onload = function(){

    //Mostrar la tabla en carga de pantalla
    peticion_movimientos.open("GET", "http://127.0.0.1:5000/api/v1.0/movimientos", true);  
    peticion_movimientos.onload = peticion_movimientos_handler  
    peticion_movimientos.onerror = function(){alert("No se ha podido completar la peticion movimientos")}  
    peticion_movimientos.send();  
}


