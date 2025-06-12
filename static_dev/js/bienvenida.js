$(document).ready(function(){
    //Oculta el título "SER-MANT" inicialmente (si no lo haces ya con CSS)
    $('.sermant-title').hide();

    // El subtítulo "ASCENSORES" ya está oculto por CSS con visibility: hidden;

    //Animar el título "SER-MANT" con fadeIn
    $('.sermant-title').fadeIn(1500, function() {
        //Cuando el fadeIn de sermant-title termina.

        // Anima el subtítulo "ASCENSORES"
        $('.ascensores-subtitle')
            .css({ 'left': '-100%', 'opacity': 0 }) // Vuelve a asegurar la posición inicial y opacidad
            .css('visibility', 'visible') // ¡Hace el elemento visible ANTES de animar!
            .animate({
                left: '0%', // Mueve a su posición final
                opacity: 1   // Desvanece a la vez
            }, 1000, function() {
                console.log("El subtítulo ASCENSORES ha llegado a su lugar.");
            });
    });


    $('.logos-slider').slick({
        infinite: true,     // Para que el carrusel se repita sin fin
        slidesToShow: 5,    // Muestra 5 elementos a la vez
        slidesToScroll: 1,  // Desliza 1 elemento por cada clic
        arrows: true,       // Muestra flechas de navegación
        dots: false,        // Oculta los puntos de navegación
        autoplay: true,     // Opcional: auto-reproducción
        autoplaySpeed: 2000, // Opcional: velocidad de auto-reproducción
        // Opcional: Configuración responsive para diferentes tamaños de pantalla
        responsive: [
            {
                breakpoint: 1024, // Para pantallas más pequeñas que 1024px
                settings: {
                    slidesToShow: 4,
                    slidesToScroll: 1
                }
            },
            {
                breakpoint: 768, // Para pantallas más pequeñas que 768px
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 1
                }
            },
            {
                breakpoint: 480, // Para pantallas más pequeñas que 480px
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1
                }
            }
        ]
    });
});