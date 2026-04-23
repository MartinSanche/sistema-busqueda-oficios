// app/static/js/main.js

// Funciones de UI reutilizables

function mostrarLoading(elementId, mensaje = 'Cargando...') {
    document.getElementById(elementId).innerHTML =
        `<p class="loading">⏳ ${mensaje}</p>`
}

function mostrarError(elementId, mensaje = 'Ocurrió un error. Intentá de nuevo.') {
    document.getElementById(elementId).innerHTML =
        `<p class="error">❌ ${mensaje}</p>`
}

function mostrarVacio(elementId, mensaje = 'No se encontraron resultados') {
    document.getElementById(elementId).innerHTML =
        `<p class="hint">${mensaje}</p>`
}