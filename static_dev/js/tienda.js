$(document).ready(function() {

    // --- Lógica de los botones +/- ---
    // Manejador para el botón de incrementar (+)
    $('.btn-increment').click(function() {
        // Encontrar el contenedor del producto que es el 'card' más cercano
        let $productCard = $(this).closest('.card');
        let $quantityInput = $productCard.find('.cantidad-input'); // Usar la nueva clase 'cantidad-input'
        let currentQuantity = parseInt($quantityInput.val());
        // Leer el stock máximo directamente del atributo 'max' del input de cantidad
        let maxStock = parseInt($quantityInput.attr('max')); // Usamos .attr() para leer el atributo HTML

        if (currentQuantity < maxStock) {
            $quantityInput.val(currentQuantity + 1);
        } else {
            console.log("No puedes agregar más, has alcanzado el stock máximo.");
            // Opcional: Mostrar un mensaje al usuario en la UI, ej. un tooltip o un texto debajo del input
        }
    });

    // Manejador para el botón de decrementar (-)
    $('.btn-decrement').click(function() {
        // Encontrar el contenedor del producto que es el 'card' más cercano
        let $productCard = $(this).closest('.card');
        let $quantityInput = $productCard.find('.cantidad-input'); // Usar la nueva clase 'cantidad-input'
        let currentQuantity = parseInt($quantityInput.val());
        // Leer el valor mínimo directamente del atributo 'min' del input
        let minQuantity = parseInt($quantityInput.attr('min'));

        if (currentQuantity > minQuantity) { // Asegurarse de que no baje del mínimo (0 en tu caso)
            $quantityInput.val(currentQuantity - 1);
        } else {
            console.log("La cantidad no puede ser menor a " + minQuantity + ".");
            // Opcional: Mostrar un mensaje al usuario
        }
    });
});