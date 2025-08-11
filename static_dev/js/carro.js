

/*-------------------------------------------------------------------------
--------- PASO 3 INCREMENTA CANTIDAD DE PRODUCTO EN LA TIENDA -------------
-------------------------------------------------------------------------*/
function Agregar(cada_producto_id, valor) {
    "use strict";
    $.ajax({
        beforeSend : function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        url : "/tienda/agregar/",
        type : "GET",
        data : { cada_producto_id:cada_producto_id, valor:valor},
        success : function (json) {
            localStorage.setItem(json[0].idproducto.toString(), json[0].cantida.toString());
            location.reload();
        },
        error : function (xhr, errmsg, err) {
            console.log('Error en carga de respuesta');
        }
    });
}
$('.agregar').click(function (event) {
    "use strict";
    event.preventDefault(); 
    let cada_producto_id = $(this).parent().get(0).id;
    let valor = $(this).parent().find('.vervalor').val();
    let i;
    for(i = 0; i < localStorage.length; i++){
        let clave_eliminar = localStorage.key(i);
        if(!clave_eliminar.startsWith("prestige_")){
            localStorage.removeItem(clave_eliminar);
        }
    }
    for(i = 0; i < localStorage.length; i++){
        let clave = localStorage.key(i);
        let el_valor = localStorage[clave];
        if(clave == cada_producto_id){
            valor = el_valor;
        }else{
            console.log("no hay coincidenciaaaa");
        }   
    }
   Agregar(cada_producto_id, valor);
});
