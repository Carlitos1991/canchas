console.log('canchas_empresa.js cargado');

// Función global para abrir modal de horarios
window.abrirModalHorarios = function(canchaId) {
    const modal = document.getElementById('modalHorarios');
    const modalBody = document.getElementById('modalHorariosBody');
    
    // Mostrar modal con spinner
    modal.classList.add('show');
    modalBody.innerHTML = `
        <div class="loading-spinner">
            <i class="fa-solid fa-spinner fa-spin"></i>
            Cargando horarios...
        </div>
    `;
    
    // Cargar horarios vía AJAX
    fetch(`/empresas/cancha/${canchaId}/horarios/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                mostrarHorarios(data.cancha, data.horarios);
            } else {
                modalBody.innerHTML = `
                    <div class="alert-error">
                        <i class="fa-solid fa-exclamation-circle"></i>
                        Error al cargar horarios
                    </div>
                `;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            modalBody.innerHTML = `
                <div class="alert-error">
                    <i class="fa-solid fa-exclamation-circle"></i>
                    Error de conexión
                </div>
            `;
        });
};

// Función para mostrar horarios en el modal
function mostrarHorarios(cancha, horarios) {
    const modalNombre = document.getElementById('modalCanchaNombre');
    const modalBody = document.getElementById('modalHorariosBody');
    
    // Actualizar nombre de cancha
    modalNombre.innerHTML = `
        <i class="fa-solid fa-calendar-days"></i>
        ${cancha.nombre} - Horarios Disponibles
    `;
    
    // Agrupar horarios por fecha
    const horariosPorFecha = {};
    horarios.forEach(h => {
        if (!horariosPorFecha[h.fecha]) {
            horariosPorFecha[h.fecha] = [];
        }
        horariosPorFecha[h.fecha].push(h);
    });
    
    // Generar HTML
    let html = '<div class="horarios-timeline">';
    
    if (Object.keys(horariosPorFecha).length === 0) {
        html += `
            <div class="no-results">
                <i class="fa-solid fa-calendar-xmark"></i>
                <p>No hay horarios disponibles</p>
            </div>
        `;
    } else {
        Object.keys(horariosPorFecha).sort().forEach(fecha => {
            const fechaObj = new Date(fecha + 'T00:00:00');
            const fechaFormato = fechaObj.toLocaleDateString('es-ES', { 
                weekday: 'long', 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
            });
            
            html += `
                <div class="dia-horarios">
                    <div class="dia-header">
                        <i class="fa-solid fa-calendar"></i>
                        ${fechaFormato.charAt(0).toUpperCase() + fechaFormato.slice(1)}
                    </div>
                    <div class="horarios-list">
            `;
            
            horariosPorFecha[fecha].forEach(horario => {
                const estadoClass = horario.estado.toLowerCase().replace('_', '-');
                const estadoTexto = {
                    'LIBRE': 'Libre',
                    'RESERVADO': 'Reservado',
                    'EN_CURSO': 'En Curso'
                }[horario.estado] || horario.estado;
                
                html += `
                    <div class="horario-item ${estadoClass}" data-horario-id="${horario.id}">
                        <span class="horario-time">
                            <i class="fa-solid fa-clock"></i>
                            ${horario.hora_inicio} - ${horario.hora_fin}
                        </span>
                        <span class="horario-estado">${estadoTexto}</span>
                        ${horario.estado === 'LIBRE' ? `
                            <button class="btn-reservar-horario" onclick="reservarHorario('${horario.id}', this)">
                                <i class="fa-solid fa-calendar-check"></i> Reservar
                            </button>
                        ` : ''}
                    </div>
                `;
            });
            
            html += `
                    </div>
                </div>
            `;
        });
    }
    
    html += '</div>';
    modalBody.innerHTML = html;
}

// Función global para cerrar modal
window.cerrarModalHorarios = function() {
    const modal = document.getElementById('modalHorarios');
    modal.classList.remove('show');
};

// Función global para reservar horario
window.reservarHorario = function(disponibilidadId, button) {
    if (!button) return;
    
    const originalText = button.innerHTML;
    button.disabled = true;
    button.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Reservando...';
    
    // Obtener CSRF token
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
                      getCookie('csrftoken');
    
    fetch('/empresas/api/reservar/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            disponibilidad_id: disponibilidadId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            button.innerHTML = '<i class="fa-solid fa-check"></i> Reservado';
            button.style.background = '#10B981';
            
            // Actualizar estado del horario
            const horarioItem = button.closest('.horario-item');
            if (horarioItem) {
                horarioItem.classList.remove('libre');
                horarioItem.classList.add('reservado');
                horarioItem.querySelector('.horario-estado').textContent = 'Reservado';
            }
            
            setTimeout(() => {
                alert('¡Reserva realizada con éxito!');
            }, 300);
        } else {
            button.disabled = false;
            button.innerHTML = originalText;
            alert(data.message || 'Error al realizar la reserva');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        button.disabled = false;
        button.innerHTML = originalText;
        alert('Error de conexión al reservar');
    });
};

// Función para filtrar canchas
window.filtrarCanchas = function() {
    const fecha = document.getElementById('fecha-buscar').value;
    const hora = document.getElementById('hora-buscar').value;
    
    const params = new URLSearchParams(window.location.search);
    
    if (fecha) {
        params.set('fecha', fecha);
    } else {
        params.delete('fecha');
    }
    
    if (hora) {
        params.set('hora', hora);
    } else {
        params.delete('hora');
    }
    
    // Recargar página con filtros
    window.location.search = params.toString();
};

// Función para limpiar filtros
window.limpiarFiltros = function() {
    document.getElementById('fecha-buscar').value = '';
    document.getElementById('hora-buscar').value = '';
    
    // Remover parámetros de URL
    const url = window.location.pathname;
    window.location.href = url;
};

// Función auxiliar para obtener cookie CSRF
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

// Cerrar modal al hacer click fuera
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('modalHorarios');
    
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                cerrarModalHorarios();
            }
        });
    }
    
    // Permitir filtrar con Enter
    const fechaInput = document.getElementById('fecha-buscar');
    const horaInput = document.getElementById('hora-buscar');
    
    [fechaInput, horaInput].forEach(input => {
        if (input) {
            input.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    filtrarCanchas();
                }
            });
        }
    });
});
