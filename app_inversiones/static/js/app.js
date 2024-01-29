console.log("Funcionando")

const version = "v1.0"
let fechaTransaccion = ""
let horaTransaccion = ""


let peticion_movimientos = new XMLHttpRequest()  //Creo un objeto de tipo XMLHttpRequest
function peticion_movimientos_handler(){       
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
            alert("Se ha producido un error en la consulta de todos los movimientos")
        }
    }                     
}


/////////////////////////////////////////////////////////////////////////////////////////////////////////


//Abrir el formulario con el boton nuevo
function viewForm(event){ 
    document.getElementById("form_detail").style.display="block"; 
}


//Cerrar el formulario con el boton cerrar
function hideForm(event){  
    event.preventDefault()  //evita que el boton cerrar envie un POST
    document.getElementById("form_detail").style.display="none";  
    document.getElementById("select_from").value=""
    document.getElementById("select_to").value=""
    document.getElementById("quantity_from").value=""
    document.getElementById("quantity_to").innerText=""
    document.getElementById("quantity_total").innerText=""
}


/////////////////////////////////////////////////////////////////////////////////////////////////////////


//Handler para obtener el exchage rate
function peticion_rate_handler(){    
    if(this.readyState === 4){
        if(this.status === 200){
            const datos = JSON.parse(this.responseText)  //captura lo que manda la peticion http. Convertimos a objeto JSON responseText y meterlo en datos  
            const quantity_from = document.getElementById("quantity_from").value             
                        
            document.getElementById("quantity_to").innerHTML=datos.rate
            document.getElementById("quantity_total").innerHTML=datos.rate*quantity_from

            //Dividir la fecha y hora del campo 'time' por el caracter T del JSON y lo guarda en el Array fechaYhora
            fechaYhora = datos.time.split('T')
            //Guardar cada parte en una variable distinta
            fechaTransaccion = fechaYhora[0]
            horaTransaccion = fechaYhora[1].replace(/\.\d+Z$/, '')  //replace saca el .0000000Z del final
            
        }else{
            alert("Se ha producido un error en la consulta de la tasa de cambio")
        }
    }
}

//Obtener el exchage rate
function getRate(event){
    event.preventDefault()  

    moneda_from = document.getElementById('select_from').value      
    moneda_to = document.getElementById('select_to').value
    
    peticion_movimientos.open("GET", `http://127.0.0.1:5000/api/${version}/tasa/${moneda_from}/${moneda_to}`, true);  
    peticion_movimientos.onload = peticion_rate_handler
    peticion_movimientos.onerror = function(){alert("No se ha podido obtener el precio de la moneda")}  
    peticion_movimientos.send();
}


/////////////////////////////////////////////////////////////////////////////////////////////////////////


//Handler y XMLHttp para nuevo registro
let peticion_nuevo_registro = new XMLHttpRequest()
function peticion_registro_handler(){
    if(this.readyState === 4){
        if(this.status === 201){  //Este es el HTTPStatus.CREATED que pasa la ruta 
            //Mostrar la tabla completa luego de guardar un movimiento nuevo
            peticion_movimientos.open("GET", `http://127.0.0.1:5000/api/${version}/movimientos`, true);  
            peticion_movimientos.onload = peticion_movimientos_handler  
            peticion_movimientos.onerror = function(){alert("No se ha podido completar la peticion movimientos")}  
            peticion_movimientos.send();  

            //Vacia los campos y cierra formulario luego de guardar un movimiento nuevo
            document.getElementById("form_detail").style.display="none";  
            document.getElementById("select_from").value=""
            document.getElementById("select_to").value=""
            document.getElementById("quantity_from").value=""
            document.getElementById("quantity_to").innerText=""
            document.getElementById("quantity_total").innerText=""
        }else{
            alert("Se ha producido un error en la consulta para guardar la inversion")
        }
    }
}

//Crear un nuevo registro
function nuevoRegistro(event){
    event.preventDefault()

    const moneda_from = document.getElementById("select_from").value
    const quantity_from = document.getElementById("quantity_from").value
    const moneda_to = document.getElementById("select_to").value
    const quantity_to = Number(document.getElementById("quantity_total").innerText).toFixed(4)

    if (moneda_from == ""){
        alert("Debe elegir una moneda para invertir")
    }
    if (moneda_to == ""){
        alert("Debe elegir una moneda para comprar")
    }
    if (quantity_from == ""){
        alert("Debe elegir un monto a invertir")
    }

    peticion_nuevo_registro.open("POST", `http://127.0.0.1:5000/api/${version}/movimiento`, true)
    peticion_nuevo_registro.onload = peticion_registro_handler
    peticion_nuevo_registro.onerror = function(){alert("No se ha podido completar la peticion")} 
    peticion_nuevo_registro.setRequestHeader("Content-Type", "application/json")  //esto es para que el post del formulario envie los datos en formato JSON

    //definir  la estructura JSON y enviar
    const datos_transaccion = JSON.stringify({
        date: fechaTransaccion,
        time: horaTransaccion,
        moneda_from: moneda_from,
        quantity_from: quantity_from, 
        moneda_to: moneda_to,
        quantity_to: quantity_to,
    })

    peticion_nuevo_registro.send(datos_transaccion)
}


/////////////////////////////////////////////////////////////////////////////////////////////////////////


window.onload = function(){

    //Guardar nuevo registro
    let confirmar = document.getElementById("btn_confirmar")
    confirmar.addEventListener("click", nuevoRegistro)

    //Mostrar formulario
    let nuevo = document.getElementById("btn_nuevo");
    nuevo.addEventListener("click", viewForm)

    //Ocultar formulario
    let cerrar = document.getElementById("btn_cerrar");
    cerrar.addEventListener("click", hideForm)

    //Mostrar exchage rate
    let rate = document.getElementById("button_calc")
    rate.addEventListener("click", getRate)

    //Mostrar la tabla en carga de pantalla
    peticion_movimientos.open("GET", `http://127.0.0.1:5000/api/${version}/movimientos`, true);  
    peticion_movimientos.onload = peticion_movimientos_handler  
    peticion_movimientos.onerror = function(){alert("No se ha podido completar la peticion movimientos")}  
    peticion_movimientos.send();  
}


