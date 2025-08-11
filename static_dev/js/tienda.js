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
            success: function(response) { // <--- COMIENZA AQUI EL REEMPLAZO
                console.log("Respuesta AJAX recibida:", response);
                const $productGrid = $('.col-md-9 > .row');
                $productGrid.empty(); // Limpia la cuadrícula actual

                // ¡AHORA! Inserta el HTML directamente de la respuesta del servidor
                if (response.html) { //
                    $productGrid.append(response.html); // Inserta el HTML renderizado por Django
                } else {
                    $productGrid.append('<div class="col-12"><p class="text-white text-center">No se encontraron productos que coincidan con tu búsqueda.</p></div>');
                }

                history.pushState(null, '', fullUrl);

                // Mantener los checkboxes marcados después del AJAX
                $('.categoria-checkbox').prop('checked', false); // Desmarcar todos primero
                params.forEach(p => { //
                    if (p.name === 'categorias') { //
                        $(`#categoria${p.value}`).prop('checked', true); // Marcar los que estaban en la petición
                    }
                });

                // ESTO ES CRUCIAL: Vuelve a inicializar los hover y cualquier otra lógica JS para los NUEVOS elementos
                // La función initializeProductImageHover() deberá estar disponible globalmente o al menos en el mismo scope.
                initializeProductImageHover(); //

                // Si tienes event listeners para los botones +/- o "Comprar" que NO usan delegación
                // (es decir, NO usan $('.col-md-9').on('click', '.btn-increment', ...)),
                // entonces también necesitarías re-aplicarlos aquí.
                // Afortunadamente, tu código ya usa delegación para estos botones (`.col-md-9').on(...)`),
                // lo cual significa que no necesitas re-inicializarlos; ¡ya funcionan para los elementos nuevos!
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
        //Reseteo a 0 el value de input name=cantidad
        $(this).closest('form').find('input[name="cantidad"]').val(0);

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

    // --- Función para animar los "img-aspect-ratio-box" de las imágenes de los productos con GSAP ---
    function initializeProductImageHover() {
        if (typeof gsap !== "undefined") {
            // Selecciona todos los div.img-aspect-ratio-box
            const imageAspectRatioBoxes = document.querySelectorAll('.card-img-container .img-aspect-ratio-box');

            imageAspectRatioBoxes.forEach(box => {
                // Crea un tween de hover PAUSADO para cada box
                const hoverTween = gsap.to(box, {
                    scale: 1.10, // Escala al 110% el div
                    duration: 0.3,
                    ease: "power1.out",
                    paused: true
                });

                // Añade los event listeners para mouseenter y mouseleave al CONTENEDOR PRINCIPAL (.card-img-container)
                // Esto es importante para que el área de hover sea toda la caja visible, no solo el div escalable
                // El padre de .img-aspect-ratio-box es <a>, y el padre de <a> es .card-img-container
                box.parentElement.parentElement.addEventListener('mouseenter', () => hoverTween.play());
                box.parentElement.parentElement.addEventListener('mouseleave', () => hoverTween.reverse());
            });
            console.log(`Animación de zoom en imágenes de producto configurada para ${imageAspectRatioBoxes.length} elementos.`);
        } else {
            console.warn("GSAP no está cargado. Las animaciones de zoom en imágenes de producto no funcionarán. Asegúrate de incluir la librería GSAP.");
        }
    }

    /*-------------------------------------------------------------------------
    --------------  IR AL CARRITO -------------------------------------
    -------------------------------------------------------------------------*/
    $('.boton_carrito').click(function() {
        for(i = 0; i < localStorage.length; i++){
            let clave_eliminar = localStorage.key(i);
            if(!clave_eliminar.startsWith("prod_")){
                localStorage.removeItem(clave_eliminar);
            }
        }
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
    });


    // Llama a la función de inicialización de los hover cuando la página carga por primera vez
    initializeProductImageHover();
    
});