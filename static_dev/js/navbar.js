$(document).ready(function() {
    // --- CÓDIGO DE GSAP ---
    // Verifica si GSAP está cargado.
    if (typeof gsap !== "undefined") {
        console.log("GSAP definido. Configurando animaciones del navbar.");

        // Deshabilita la restauración de scroll del navegador para evitar el "pestañeo" inicial.
        gsap.core.globals.scrollRestoration = "none";

        // ANIMACIÓN PARA TODOS LOS <a> DENTRO DE .mi_navbar ---
        const zoomHoverElements = document.querySelectorAll(".mi_navbar a");

        if (zoomHoverElements.length > 0) {
            zoomHoverElements.forEach(element => {
                // Crea un tween de hover PAUSADO para cada <a>
                const hoverTween = gsap.to(element, {
                    scale: 1.05, // Aumenta el tamaño al 105%
                    duration: 0.2,
                    paused: true,
                    ease: "power1.out"
                });

                element.addEventListener("mouseenter", () => hoverTween.play());
                element.addEventListener("mouseleave", () => hoverTween.reverse());
            });
            console.log(`Animación de zoom en hover configurada para ${zoomHoverElements.length} enlaces.`);
        } else {
            console.warn("No se encontraron elementos <a> dentro de '.mi_navbar'.");
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

    } else {
        // Mensaje de error más específico
        console.error("GSAP no está cargado. Animaciones del navbar deshabilitadas."); 
    }
});