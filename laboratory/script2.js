document.addEventListener("DOMContentLoaded", () => {
    const videoPlayer = document.querySelector('.video_player');
    const appVideos = document.querySelector('.app_videos');

    // Función para calcular y aplicar el ancho en tiempo real
    const updateVideoWidth = () => {
        // Verificar si el ancho de la ventana es menor a 280px
        if (window.innerWidth < 280) {
            // Obtener el alto del video
            const videoHeight = videoPlayer.videoHeight;

            // Calcular el ancho según la relación de aspecto 9:16
            const aspectRatio = 9 / 16;
            let calculatedWidth = videoHeight * aspectRatio;

            // Dividir el ancho calculado por 2
            calculatedWidth /= 2;

            // Aplicar el ancho calculado al contenedor
            appVideos.style.width = `${calculatedWidth}px`;

            // Opcional: mostrar resultados en la consola
            console.log(`Altura del video: ${videoHeight}px`);
            console.log(`Ancho calculado (mitad): ${calculatedWidth}px`);
        }
    };

    // Actualizar el ancho cuando el video esté listo
    videoPlayer.addEventListener('loadedmetadata', updateVideoWidth);

    // Actualizar el ancho cuando se cambie el tamaño de la ventana
    window.addEventListener('resize', updateVideoWidth);
});








// Seleccionamos todos los videos para alternar entre play y pause
const videos = document.querySelectorAll('.video_player');
        
// Evento de clic en cada video
videos.forEach(video => {
    video.addEventListener('click', () => {
        if (video.paused) {
            video.play();  // Reproducimos el video
            video.muted = false;
        } else {
            video.pause();  // Pausamos el video
        }
    });
});

// Seleccionamos todos los contenedores de sonido
const soundIcons = document.querySelectorAll('.sound');

soundIcons.forEach(icon => {
    icon.addEventListener('click', () => {
        // Determinamos si todos los videos deben ser muteados o desmuteados
        const videos = document.querySelectorAll('.video_player');
        const anyUnmuted = Array.from(videos).some(video => !video.muted);

        // Alternamos el estado de muted en todos los videos
        videos.forEach(video => {
            video.muted = anyUnmuted; // Si alguno está desmuteado, muteamos todos
        });

        // Cambiamos el ícono de sonido en todos los botones
        soundIcons.forEach(soundIcon => {
            const soundSymbol = soundIcon.querySelector('.material-symbols-outlined');
            soundSymbol.textContent = anyUnmuted ? 'volume_off' : 'volume_up';
        });
    });
});


// Configuración del Intersection Observer
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        const video = entry.target;

        if (entry.isIntersecting) {
            // Si el video está visible en el viewport
            console.log(`El video "${video.src}" está en primer plano.`);
            video.play(); // Opcional: Puedes reproducir el video automáticamente
        } else {
            // Si el video ya no está visible
            // console.log(`El video "${video.src}" no está en primer plano.`);
            video.currentTime = 0;
            video.pause(); // Opcional: Puedes pausar el video automáticamente
        }
    });
}, {
    threshold: 0.5 // El porcentaje de visibilidad necesario (50% en este caso)
});

// Selecciona todos los videos
const videos1 = document.querySelectorAll('.video_player');

// Observa cada video
videos1.forEach(video => {
    observer.observe(video);
});



// Eliminamos la declaración duplicada de `utterance`
// Inicializamos el objeto SpeechSynthesisUtterance
const initialUtterance = new SpeechSynthesisUtterance("Hola, este es un lector de pantalla, activa el audio dando click al centro de la pantalla para crear una cuenta da presiona abajo a la derecha");
initialUtterance.lang = 'es-ES'; // Español
speechSynthesis.speak(initialUtterance);

// Configuramos los botones de leer y detener
const readTextButton = document.getElementById('readText');
const stopTextButton = document.getElementById('stopText');

// Inicializamos SpeechSynthesis
const synth = window.speechSynthesis;

// Función para obtener todo el texto del documento
function getAllText() {
    return document.body.innerText;
}

// Función para leer el texto
function readText() {
    // Obtener el texto del HTML
    const text = getAllText();

    // Crear una instancia de SpeechSynthesisUtterance
    const utterance = new SpeechSynthesisUtterance(text);

    // Configurar opciones (puedes personalizar el idioma y velocidad)
    utterance.lang = 'es-ES'; // Español
    utterance.rate = 1; // Velocidad (1 = normal)

    // Habilitar el botón de detener y deshabilitar el de leer
    readTextButton.disabled = true;
    stopTextButton.disabled = false;

    // Leer el texto
    synth.speak(utterance);

    // Cuando termine de hablar, habilitar el botón de leer
    utterance.onend = () => {
        readTextButton.disabled = false;
        stopTextButton.disabled = true;
    };

    // Si se detiene la lectura manualmente
    utterance.onerror = () => {
        readTextButton.disabled = false;
        stopTextButton.disabled = true;
    };
}

// Función para detener la lectura
function stopText() {
    synth.cancel();
    readTextButton.disabled = false;
    stopTextButton.disabled = true;
}

// Asociar eventos a los botones
readTextButton.addEventListener('click', readText);
stopTextButton.addEventListener('click', stopText);