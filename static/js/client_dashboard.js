async function reservarHorario(id, btnElement) {
    if (!confirm('¿Confirmar reserva para este horario?')) return;

    const originalText = btnElement.innerText;
    btnElement.disabled = true;
    btnElement.innerText = 'Reservando...';

    // Obtenemos la URL del atributo data del botón (Mejor práctica)
    const url = btnElement.dataset.url;

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Usamos el helper
            },
            body: JSON.stringify({disponibilidad_id: id})
        });

        const data = await response.json();

        if (data.success) {
            const item = btnElement.closest('.disponibilidad-item-client');
            item.innerHTML = '<span class="text-success"><i class="fa-solid fa-check"></i> Reservado</span>';
        } else {
            alert('Error: ' + data.message);
            btnElement.disabled = false;
            btnElement.innerText = originalText;
        }
    } catch (error) {
        console.error(error);
        alert('Ocurrió un error de conexión');
        btnElement.disabled = false;
        btnElement.innerText = originalText;
    }
}