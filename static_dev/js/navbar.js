
    // --- CÓDIGO DE GSAP Y SCROLLTRIGGER ---
    if (typeof gsap !== "undefined" && typeof ScrollTrigger !== "undefined") {
        console.log("2. GSAP y ScrollTrigger definidos. Registrando plugin."); 
        gsap.registerPlugin(ScrollTrigger);

        // Deshabilita la restauración de scroll del navegador para evitar el "pestañeo" inicial.
        gsap.core.globals.scrollRestoration = "none";

        // ANIMACIÓN PARA TODOS LOS <a> DENTRO DE .mi_navbar ---
        // Selecciona TODOS los elementos <a> dentro de .mi_navbar
        const zoomHoverElements = document.querySelectorAll(".mi_navbar a");

        if (zoomHoverElements.length > 0) {
            zoomHoverElements.forEach(element => {
            // Crea un tween de hover PAUSADO para cada <a>
            const hoverTween = gsap.to(element, {
                scale: 1.05, // Aumenta el tamaño al 115%
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
        $(window).on('load', function() {
            console.log("5. Ventana cargada - Refrescando ScrollTrigger."); 
            ScrollTrigger.refresh();
            window.scrollTo(0, 0);
        });
    } else {
        console.error("GSAP o ScrollTrigger no están cargados. Animaciones HR deshabilitadas."); 
    }
