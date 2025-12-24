console.log('gestion.js cargado');

// --- Helper CSRF (Seguridad) ---
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

// --- Funciones Globales para los Botones (FUERA del DOMContentLoaded) ---

window.openModal = function (modalId) {
    console.log('openModal llamado con:', modalId);
    const modal = document.getElementById(modalId);
    console.log('Modal encontrado:', modal);
    
    if (modal) {
        modal.classList.add('show');
        console.log('Clase "show" agregada al modal');
        
        // Si es el modal de empresa, preparar para nueva empresa
        if (modalId === 'modalEmpresa') {
            const form = modal.querySelector('form');
            if (form) {
                form.reset();
                // Limpiar el campo oculto de empresa_id para crear nueva
                const empresaIdInput = document.getElementById('empresa_id');
                if (empresaIdInput) empresaIdInput.value = '';
                
                // Cambiar título
                const titulo = document.getElementById('tituloModalEmpresa');
                if (titulo) titulo.textContent = 'Nueva Empresa';
            }
        }
        // Solo resetear si es un formulario de "nuevo", no de "editar"
        else if (!modalId.includes('Cancha')) {
            const form = modal.querySelector('form');
            if (form) form.reset();
        }
    } else {
        console.error("No se encontró el modal:", modalId);
    }
}

window.closeModal = function (modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.remove('show');
}

// --- Función para Editar Empresa ---
window.editarEmpresa = function (id, nombre, gerente, telefono, direccion, ubicacionUrl) {
    console.log("Editando empresa:", id, nombre);
    
    // Cambiar título del modal
    const titulo = document.getElementById('tituloModalEmpresa');
    if (titulo) titulo.textContent = 'Editar Empresa';
    
    // Asignar valores a los inputs
    const empresaIdInput = document.getElementById('empresa_id');
    const nombreInput = document.getElementById('id_nombre_empresa');
    const gerenteInput = document.getElementById('id_gerente');
    const telefonoInput = document.getElementById('id_telefono');
    const direccionInput = document.getElementById('id_direccion');
    const ubicacionInput = document.getElementById('id_ubicacion_url');
    
    if (empresaIdInput) empresaIdInput.value = id;
    if (nombreInput) nombreInput.value = nombre;
    if (gerenteInput) gerenteInput.value = gerente;
    if (telefonoInput) telefonoInput.value = telefono;
    if (direccionInput) direccionInput.value = direccion;
    if (ubicacionInput) ubicacionInput.value = ubicacionUrl || '';
    
    openModal('modalEmpresa');
}

// --- Lógica Editar Cancha ---
window.editarCancha = function (id, nombre, capacidad, precio) {
    console.log("Editando cancha:", id, nombre);

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

console.log('Funciones globales definidas');

// --- Eventos que SÍ necesitan esperar al DOM ---
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOMContentLoaded ejecutado en gestion.js');

    // --- Cerrar al hacer click fuera ---
    document.addEventListener('click', function (event) {
        // Solo cerrar modales de gestion.js, NO los modales de admin_usuarios
        if (event.target.classList.contains('modal') && 
            !event.target.classList.contains('modal-usuarios') &&
            !event.target.classList.contains('modal-overlay')) {
            console.log('gestion.js cerrando modal:', event.target.id);
            event.target.classList.remove('show');
        } else if (event.target.classList.contains('modal')) {
            console.log('gestion.js detectó modal pero NO lo cierra (es modal-usuarios o modal-overlay):', event.target.id);
        }
    });

    // --- Envío de Formularios AJAX ---
    const forms = document.querySelectorAll('.ajax-form');
    forms.forEach(form => {
        form.addEventListener('submit', async function (e) {
            e.preventDefault();

            const formData = new FormData(this);
            
            // Determinar la URL según el formulario
            let url = this.action;
            
            // Si es el formulario de empresa y no tiene action, usar la URL correcta
            if (this.id === 'formEmpresa') {
                url = '/empresas/save-empresa/';
            }

            const btn = this.querySelector('button[type="submit"]');
            const originalText = btn.innerHTML;

            btn.disabled = true;
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Guardando...';

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
                    // Mostrar mensaje de éxito
                    alert(data.message || '¡Guardado exitosamente!');
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
                btn.innerHTML = originalText;
            }
        });
    });
});