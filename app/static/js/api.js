// app/static/js/api.js
// Módulo central para todas las llamadas a la API

const API = {

    // URL base de la API
    baseUrl: '/api',

    // Función genérica para hacer peticiones
    async get(endpoint) {
        try {
            const response = await fetch(this.baseUrl + endpoint)
            if (!response.ok) {
                throw new Error(`Error ${response.status}: ${response.statusText}`)
            }
            return await response.json()
        } catch (error) {
            console.error('Error en la API:', error)
            throw error
        }
    },

    // Obtener todos los oficios
    async getOficios() {
        return await this.get('/oficios')
    },

    // Buscar profesionales
    async buscar(oficio = '', ubicacion = '') {
        const params = new URLSearchParams()
        if (oficio)    params.append('oficio', oficio)
        if (ubicacion) params.append('ubicacion', ubicacion)
        return await this.get(`/buscar?${params.toString()}`)
    },

    // Obtener detalle de un profesional
    async getProfesional(id) {
        return await this.get(`/profesional/${id}`)
    }
}