document.addEventListener('DOMContentLoaded', () => {

    // --- Helper CSRF (Seguridad) ---
    // Lo incluimos aquí por seguridad si main.js no carga primero
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // --- Funciones Globales para los Botones (window.func) ---

    window.openModal = function (modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('show');
            // Resetear formularios al abrir (opcional pero recomendado)
            const form = modal.querySelector('form');
            // Solo resetear si es un formulario de "nuevo", no de "editar"
            if (form && !modalId.includes('Cancha')) {
                form.reset();
            }
        } else {
            console.error("No se encontró el modal:", modalId);
        }
    }

    window.closeModal = function (modalId) {
        const modal = document.getElementById(modalId);
        if (modal) modal.classList.remove('show');
    }

    // --- Lógica Editar Cancha ---
    window.editarCancha = function (id, nombre, capacidad, precio) {
        console.log("Editando cancha:", id, nombre); // Debug

        // Asignar valores a los inputs
        // Gracias al paso 2, estos IDs ahora existen seguro
        const idInput = document.getElementById('edit_cancha_id');
        const nombreInput = document.getElementById('id_nombre_cancha');
        const capInput = document.getElementById('id_capacidad');
        const precioInput = document.getElementById('id_precio_hora');

        if (idInput) idInput.value = id;
        if (nombreInput) nombreInput.value = nombre;
        if (capInput) capInput.value = capacidad;
        if (precioInput) precioInput.value = precio;

        openModal('modalCancha');
    }

    window.openDisponibilidadModal = function (canchaId) {
        const input = document.getElementById('disp_cancha_id');
        if (input) input.value = canchaId;
        openModal('modalDisponibilidad');
    }

    // --- Cerrar al hacer click fuera ---
    window.onclick = function (event) {
        if (event.target.classList.contains('modal')) {
            event.target.classList.remove('show');
        }
    }

    // --- Envío de Formularios AJAX ---
    const forms = document.querySelectorAll('.ajax-form');
    forms.forEach(form => {
        form.addEventListener('submit', async function (e) {
            e.preventDefault();

            const formData = new FormData(this);
            const url = this.action;
            const btn = this.querySelector('button[type="submit"]');
            const originalText = btn.innerText;

            btn.disabled = true;
            btn.innerText = 'Guardando...';

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                });

                const data = await response.json();

                if (data.success) {
                    location.reload(); // Éxito: Recargar página
                } else {
                    // Mostrar errores
                    let errorMsg = "Error al guardar:\n";
                    if (data.errors) {
                        for (const [key, value] of Object.entries(data.errors)) {
                            errorMsg += `${key}: ${value}\n`;
                        }
                    } else {
                        errorMsg += data.message || "Error desconocido";
                    }
                    alert(errorMsg);
                }
            } catch (error) {
                console.error(error);
                alert('Error de conexión con el servidor.');
            } finally {
                btn.disabled = false;
                btn.innerText = originalText;
            }
        });
    });
});