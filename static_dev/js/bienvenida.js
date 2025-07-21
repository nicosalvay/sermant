$(document).ready(function(){
    console.log("1. DOM listo - jQuery ready se ha disparado.");


    // Oculta el título "SER-MANT" inicialmente (si no lo haces ya con CSS)
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

    // Inicialización del slider Slick
    $('.logos-slider').slick({
        infinite: true,
        slidesToShow: 5,
        slidesToScroll: 1,
        arrows: true,
        dots: false,
        autoplay: true,
        autoplaySpeed: 2000,
        responsive: [
            { breakpoint: 1024, settings: { slidesToShow: 4, slidesToScroll: 1 } },
            { breakpoint: 768, settings: { slidesToShow: 3, slidesToScroll: 1 } },
            { breakpoint: 480, settings: { slidesToShow: 2, slidesToScroll: 1 } }
        ]
    });

    // --- CÓDIGO DE GSAP Y SCROLLTRIGGER ---
    if (typeof gsap !== "undefined" && typeof ScrollTrigger !== "undefined") {
        console.log("2. GSAP y ScrollTrigger definidos. Registrando plugin."); 
        gsap.registerPlugin(ScrollTrigger);

        // Deshabilita la restauración de scroll del navegador para evitar el "pestañeo" inicial.
        gsap.core.globals.scrollRestoration = "none";
  
        // Lista de contenedores
        const seccionContenedores = document.querySelectorAll("#contenedor-quienes-somos, #logos-div-principal, #contenedor-contactanos"); 
        
        console.log("3. Contenedores de sección animados encontrados:", seccionContenedores.length);

        seccionContenedores.forEach(contenedor => {
            console.log("4. Configurando animación para contenedor:", contenedor);

            let elementosAAnimar;

            if (contenedor.id === "contenedor-quienes-somos") {
                elementosAAnimar = contenedor.querySelectorAll(".quienes-somos-titulo, .quienes-somos-texto, #carousel-trabajos-container h3, #carousel-trabajos-container .carousel-inner");
            } else if (contenedor.id === "logos-div-principal") {
                elementosAAnimar = contenedor.querySelectorAll("h3, .logos-slider");
            } else if (contenedor.id === "contenedor-contactanos") { 
                elementosAAnimar = contenedor.querySelectorAll("h1, h3, .mb-3, button[type='submit']"); 
                
            }
            
            if (elementosAAnimar && elementosAAnimar.length > 0) {
                gsap.to(elementosAAnimar, { 
                    opacity: 1,
                    visibility: "visible",
                    y: 0, 
                    duration: 0.8,
                    stagger: 0.1, 
                    ease: "power2.out", 
                    scrollTrigger: {
                        trigger: contenedor, 
                        start: "top 80%",
                        end: "top 80%",    
                        toggleActions: "play none reverse none", 
                        markers: false 
                    },
                    onComplete: function() {
                        console.log("Animación de aparición de elemento completada para:", this.targets()[0]);
                    }
                });
            } else {
                console.warn("No se encontraron elementos para animar dentro del contenedor:", contenedor.id);
            }
        });

        const hrElements = document.querySelectorAll(".linea-solida");
        console.log("3. Elementos HR encontrados:", hrElements.length); 

        hrElements.forEach(hr => {
            console.log("4. Configurando animación para HR:", hr); 
            gsap.to(hr, {
                opacity: 1,
                visibility: "visible",
                duration: 1,
                scrollTrigger: {
                    trigger: hr,
                    start: "top 80%",
                    end: "top 80%",
                    toggleActions: "play none reverse none",
                    markers: false 
                }
            });
        });

        // ANIMACIÓN PARA MÚLTIPLES BOTONES/IMÁGENES CON HOVER ---
        // Selecciona TODOS los elementos que tienen la clase 'anim-zoom-hover'
        const zoomHoverElements = document.querySelectorAll(".anim-zoom-hover");

        if (zoomHoverElements.length > 0) {
            zoomHoverElements.forEach(element => {
                // Crea un tween de hover PAUSADO para cada elemento individualmente
                const hoverTween = gsap.to(element, {
                    scale: 1.15, // Aumenta el tamaño al 115%
                    duration: 0.2, // Duración de la animación de entrada
                    paused: true, // Muy importante: no se ejecuta hasta que lo llamemos
                    ease: "power1.out" // Suavizado
                });

                // Añade los eventos de mouse para cada elemento
                element.addEventListener("mouseenter", () => hoverTween.play());
                element.addEventListener("mouseleave", () => hoverTween.reverse());
            });
            console.log(`8. Animación de zoom en hover configurada para ${zoomHoverElements.length} elementos.`);
        } else {
            console.warn("No se encontraron elementos con la clase 'anim-zoom-hover'.");
        }       

        $(window).on('load', function() {
            console.log("5. Ventana cargada - Refrescando ScrollTrigger."); 
            ScrollTrigger.refresh();
            window.scrollTo(0, 0);
        });
    } else {
        console.error("GSAP o ScrollTrigger no están cargados. Animaciones HR deshabilitadas."); 
    }
});