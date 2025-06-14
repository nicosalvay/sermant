$(document).ready(function() {

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
    
    // --- Función para actualizar la interfaz con los productos filtrados ---
    function updateProductList(productos) {
        const $productGrid = $('.col-md-9 > .row'); 
        $productGrid.empty(); 

        if (productos.length === 0) {
            $productGrid.append('<div class="col-12"><p class="text-white text-center">No se encontraron productos que coincidan con tu búsqueda.</p></div>');
            return;
        } 
        
        productos.forEach(function(producto) {
            const detalleUrl = `/tienda/${producto.id}/ver/`;
            
            const productCard = `
                <div class="col-md-4 mb-4">
                    <div class="card">
                        <div class="card-img-container">
                            <a href="${detalleUrl}">
                                <img src="${producto.imagen_url}" class="card-img-top" alt="${producto.producto}">
                            </a>
                        </div>
                        <div class="card-body text-center card-body-ventas">
                            <hr>
                            <h5 class="card-title">${producto.producto}</h5>
                            <p class="card-text descripcion-producto">${producto.descripcion}</p>
                            <p class="card-text precios">$${producto.precio}</p>
                            
                            <form class="add-to-cart-form" action="{% url 'venta_productos' %}" method="post">
                                <input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}">
                                <input hidden type="text" name="producto" value="prod_${producto.id}"/>
                                <div class="input-group mb-3 justify-content-center">
                                    <button class="btn btn-outline-secondary btn-decrement" type="button">-</button>
                                    <input type="number" name="cantidad" class="form-control text-center cantidad-input" value="0" min="0" max="${producto.stock}" style="max-width: 70px;">
                                    <button class="btn btn-outline-secondary btn-increment" type="button">+</button>
                                </div>
                                <input type="button" class="float-right btn btn-primary add-to-cart-button" value="Comprar"/>
                                
                            </form>
                        </div>
                    </div>
                </div>
            `;
            $productGrid.append(productCard);
        });
    }

    // Manejar el envío del formulario de búsqueda con AJAX
    $('#search-form').submit(function(e) {
        e.preventDefault(); // Evita la recarga de la página

        const $form = $(this);
        const url = $form.attr('action') || window.location.pathname;
        
        // --- RECOLECCIÓN MANUAL DE DATOS ---
        let params = [];

        // Recoger el valor del input de búsqueda (que sí está en el search-form)
        const querycom_val = $form.find('input[name="querycom"]').val();
        if (querycom_val) {
            params.push({ name: 'querycom', value: querycom_val });
        }

        // Recoger los valores de los checkboxes de categoría
        // Buscamos todos los checkboxes con la clase 'categoria-checkbox' que estén :checked
        $('.categoria-checkbox:checked').each(function() {
            params.push({ name: 'categorias', value: $(this).val() });
        });

        // Recoger los valores de los inputs de precio
        const precioDesde = $('#precioDesde').val();
        if (precioDesde) {
            params.push({ name: 'precioDesde', value: precioDesde });
        }
        const precioHasta = $('#precioHasta').val();
        if (precioHasta) {
            params.push({ name: 'precioHasta', value: precioHasta });
        }
     
        // Convertir el array de parámetros a un string de URL query (ej. param1=valor1&param2=valor2)
        const fullUrlParams = new URLSearchParams(params.map(p => [p.name, p.value])).toString();
        const fullUrl = `${url}?${fullUrlParams}`;

        // Realizar la petición AJAX
        $.ajax({
            url: fullUrl,
            type: 'GET',
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            dataType: 'json',
            beforeSend: function() {
                console.log("Enviando petición de filtrado (AJAX) con datos manuales...");
                // Ver después de poner un spinner aquí
            },
            success: function(response) {
                console.log("Productos filtrados recibidos (AJAX):", response.productos);
                updateProductList(response.productos);
                // Actualizar la URL del navegador sin recargar la página (para que sea compartible)
                history.pushState(null, '', fullUrl); 

                // Mantener los checkboxes marcados después del AJAX
  
                $('.categoria-checkbox').prop('checked', false); // Desmarcar todos primero
                params.forEach(p => {
                    if (p.name === 'categorias') {
                        $(`#categoria${p.value}`).prop('checked', true); // Marcar los que estaban en la petición
                    }
                });
            },
            error: function(xhr, status, error) {
                console.error("Error al filtrar productos (AJAX):", status, error, xhr.responseText);
                alert("Ocurrió un error al filtrar los productos.");
            },
            complete: function() {
                // Ocultar spinner cuando lo ponga
            }
        });
    });

    // Disparar el filtro cuando se cambian los checkboxes de categoría ---
    $('.card-body').on('change', '.categoria-checkbox', function() {
        // Cuando un checkbox de categoría cambia, disparamos el submit del formulario principal.
        $('#search-form').submit(); // Esto ejecutará la función AJAX de arriba
    });

    // Manejar el clic en el botón de filtrar del panel lateral
    $('#filtrar').on('click', function() {
        $('#search-form').submit(); // Esto también ejecutará la función AJAX de arriba
    });

    // Lógica de Autocompletado
    $('#id_querycom').autocomplete({
        source: AUTOCMPLETE_URL,
        minLength: 2,
        select: function(event, ui) {
            $('#id_querycom').val(ui.item.label);
            // Al seleccionar del autocompletado, disparar el filtro AJAX
            $('#search-form').submit(); 
        }
    });

    // --- Lógica de los botones +/- ---
    $('.col-md-9').on('click', '.btn-increment', function() {
        const $input = $(this).siblings('.cantidad-input');
        let currentQuantity = parseInt($input.val());
        const maxStock = parseInt($input.attr('max'));
        if (!isNaN(currentQuantity) && currentQuantity < maxStock) {
            $input.val(currentQuantity + 1);
        } else {
            console.log("No puedes agregar más, has alcanzado el stock máximo.");
        }
    });

    $('.col-md-9').on('click', '.btn-decrement', function() {
        const $input = $(this).siblings('.cantidad-input');
        let currentQuantity = parseInt($input.val());
        const minQuantity = parseInt($input.attr('min'));
        if (!isNaN(currentQuantity) && currentQuantity > minQuantity) {
            $input.val(currentQuantity - 1);
        } else {
            console.log("La cantidad no puede ser menor a " + minQuantity + ".");
        }
    });

    // --- Tu lógica del botón "Comprar" y `AgregarI` 
    $('.col-md-9').on('click', '.add-to-cart-button', function (event) {
        "use strict";
        event.preventDefault();

        let cada_producto_id = $(this).closest('form').find('input[name="producto"]').val();
        let valor = $(this).closest('form').find('input[name="cantidad"]').val();

        console.log('Desde .agregar: ', cada_producto_id);
        console.log('Desde .agregar: ', valor);

        // PASO 1: Remuevo todo item que no inicia con prod_
        console.log(JSON.stringify(localStorage));
        let i;
        for(i = 0; i < localStorage.length; i++){
            let clave_eliminar = localStorage.key(i);
            if(!clave_eliminar.startsWith("prod_")){
                localStorage.removeItem(clave_eliminar);
            }
        }

        let cantidadGuardada = localStorage.getItem(cada_producto_id);
        if (cantidadGuardada === null) {
            cantidadGuardada = 0;
        }
        console.log('Cantidad guardada en localStorage:', cantidadGuardada);

        AgregarI(cada_producto_id, valor, cantidadGuardada);
    });

    // Función AgregarI
    function AgregarI(cada_producto_id, valor, cantidadGuardada) {
        "use strict";
        console.log("Llamando a AgregarI:", cada_producto_id, valor, cantidadGuardada);
        $.ajax({
            url : "/tienda/agregar/",
            type : "GET", 
            data : { cada_producto_id:cada_producto_id, valor:valor,
                     cantidadGuardada:cantidadGuardada },
            success : function (json) {
                console.log(json[0].idproducto.toString());
                console.log(json[0].cantida.toString());
                localStorage.setItem(json[0].idproducto.toString(),
                json[0].cantida.toString());
                
            },
            error : function (xhr, errmsg, err) {
                console.log('Error en carga de respuesta: ' + errmsg);
            }
        });
    } 
});