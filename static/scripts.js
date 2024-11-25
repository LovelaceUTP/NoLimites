document.addEventListener("DOMContentLoaded", () => {
    const videoPlayer = document.querySelector('.video_player');
    const popupInicial = document.getElementById("popup-inicial"); // Primer pop-up
    const popup = document.getElementById("popup"); // Segundo pop-up
    const respuestaSi = document.getElementById("respuesta-si");
    const respuestaNo = document.getElementById("respuesta-no");
    const permitirBtn = document.getElementById("permitir");
    const denegarBtn = document.getElementById("denegar");

    // Mostrar los pop-ups secuencialmente
    window.onload = function() {
        if (!sessionStorage.getItem("popupInicialShown")) {
            popupInicial.style.display = "flex"; // Mostrar el primer pop-up

            respuestaSi.addEventListener("click", function() {
                popupInicial.style.display = "none"; // Cerrar el primer pop-up
                mostrarPopupSecundario();
                sessionStorage.setItem("popupInicialShown", "true"); // Marcar que el primer pop-up fue mostrado
            });

            respuestaNo.addEventListener("click", function() {
                popupInicial.style.display = "none"; // Cerrar el primer pop-up
                mostrarPopupSecundario();
                sessionStorage.setItem("popupInicialShown", "true"); // Marcar que el primer pop-up fue mostrado
            });
        } else {
            mostrarPopupSecundario(); // Mostrar el segundo pop-up directamente si el primero ya se mostró
        }
    };

    // Mostrar el segundo pop-up
    function mostrarPopupSecundario() {
        if (!sessionStorage.getItem("popupShown")) {
            popup.style.display = "flex"; // Mostrar el segundo pop-up

            permitirBtn.addEventListener("click", function() {
                solicitarUbicacion();
                popup.style.display = "none"; // Cerrar el segundo pop-up
                sessionStorage.setItem("popupShown", "true"); // Marcar que el segundo pop-up fue mostrado
            });

            denegarBtn.addEventListener("click", function() {
                popup.style.display = "none"; // Cerrar el segundo pop-up
                sessionStorage.setItem("popupShown", "true"); // Marcar que el segundo pop-up fue mostrado
            });
        }
    }

    // Función para calcular y aplicar el ancho en tiempo real
    const updateVideoWidth = () => {
        if (window.innerWidth < 280) {
            const videoHeight = videoPlayer.videoHeight;
            const aspectRatio = 9 / 16;
            let calculatedWidth = videoHeight * aspectRatio;
            calculatedWidth /= 2;
            videoPlayer.style.width = `${calculatedWidth}px`; // Ajustar el tamaño del video
        }
    };

    // Evento para cargar el video y calcular el tamaño
    videoPlayer.addEventListener('loadedmetadata', updateVideoWidth);

    // Solicitar la ubicación del usuario
    function solicitarUbicacion() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const latitude = position.coords.latitude;
                    const longitude = position.coords.longitude;
                    console.log(`Latitud: ${latitude}, Longitud: ${longitude}`);
                },
                (error) => {
                    console.error(`Error al obtener ubicación: ${error.message}`);
                },
                {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 0
                }
            );
        } else {
            console.error("La geolocalización no está soportada en este navegador.");
        }
    }

    // Configuración del Intersection Observer
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            const video = entry.target;
            if (entry.isIntersecting) {
                video.play(); // Reproducir cuando el video esté visible
            } else {
                video.currentTime = 0;
                video.pause(); // Pausar cuando no está visible
            }
        });
    }, {
        threshold: 0.5
    });

    // Observar todos los videos
    const videos1 = document.querySelectorAll('.video_player');
    videos1.forEach(video => {
        observer.observe(video);
    });
});

// Manejar el clic en cada video
const videos = document.querySelectorAll('.video_player');
videos.forEach(video => {
    video.addEventListener('click', () => {
        if (video.paused) {
            video.muted = false;
            video.play();  // Reproducimos el video
        } else {
            video.muted = true;
            video.pause();  // Pausamos el video
        }
    });
});
