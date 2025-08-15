
/*..............................................................................................
... PARA VALIDAR LOS DATOS .....................................................
.............................................................................................*/
var csrftoken = $.cookie('csrftoken');
function csrfSafeMethod(method) {
    "use strict";
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}   

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

/*-------------------------------------------------------------------------
---------  INCREMENTAR CANTIDAD DE PRODUCTO EN LA TIENDA -------------
-------------------------------------------------------------------------*/
function Agregar(cada_producto_id, valor) {
    "use strict";
    $.ajax({        
        url : "/carrito/agregar/",
        type : "GET",
        data : { cada_producto_id:cada_producto_id, valor:valor},
        success : function (json) {
            localStorage.setItem(json[0].idproducto.toString(), json[0].cantidad.toString());
            location.reload();
        },
        error : function (xhr, errmsg, err) {
            console.log('Error en carga de respuesta');
        }
    });
}

$('.btn-increment').click(function (event) {
    "use strict";
    event.preventDefault(); 
    let cada_producto_id = $(this).closest('form').find('input[name="producto"]').val();
    let valor = $(this).parent().find('.cantidad-input').val();
    let i;
    for(i = 0; i < localStorage.length; i++){
        let clave_eliminar = localStorage.key(i);
        if(!clave_eliminar.startsWith("prod_")){
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

/*-------------------------------------------------------------------------
---------  QUITAR CANTIDAD DE PRODUCTO EN LA TIENDA -------------
-------------------------------------------------------------------------*/
function Quitar(cada_producto_id, valor) {
    "use strict";
    $.ajax({        
        url : "/carrito/quitar/",
        type : "GET",
        data : { cada_producto_id:cada_producto_id, valor:valor},
		success : function (json) {
            $('#'+json[0].idproducto +' .cantidad-input').val(json[0].cantidad);
            let cant = json[0].cantidad
            if (cant == 0){
                console.log("vacío");
                localStorage.removeItem(json[0].idproducto.toString(), json[0].cantidad.toString());
                $.ajax({
                    url: "/tienda/crear_localstorage/",
                    data:{producto : JSON.stringify(localStorage)},
                    type: 'get',
                    dataType: 'json',
                    contentType: 'application/json',
                    success: function (data) {
                        var urla = window.location.origin + "/carrito";    
                        window.location.href = urla;
                    },
                });
                location.reload();
            }else{
                localStorage.setItem(json[0].idproducto.toString(), json[0].cantidad.toString());
                location.reload();
            }
            location.reload();
		},
        error : function (xhr, errmsg, err) {
            console.log('Error en carga de respuesta');
        }
    });
}

$('.btn-decrement').click(function (event) {
    "use strict";
    event.preventDefault(); 
    let cada_producto_id = $(this).closest('form').find('input[name="producto"]').val();
    let valor = $(this).parent().find('.cantidad-input').val();
    let i;
    for(i = 0; i < localStorage.length; i++){
        let clave_eliminar = localStorage.key(i);
        if(!clave_eliminar.startsWith("prod_")){
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
   Quitar(cada_producto_id, valor);
});
