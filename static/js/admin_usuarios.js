// JavaScript para la gestión de usuarios

// Búsqueda en tiempo real
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const filterButtons = document.querySelectorAll('.filter-btn');
    const tableRows = document.querySelectorAll('#usersTableBody tr');
    
    let currentFilter = 'all';
    
    // Búsqueda
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            filterAndSearch(searchTerm, currentFilter);
        });
    }
    
    // Filtros por rol
    filterButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            // Remover clase active de todos los botones
            filterButtons.forEach(b => b.classList.remove('active'));
            // Agregar clase active al botón clickeado
            this.classList.add('active');
            
            currentFilter = this.dataset.filter;
            const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
            filterAndSearch(searchTerm, currentFilter);
        });
    });
    
    function filterAndSearch(searchTerm, filter) {
        tableRows.forEach(row => {
            const userName = row.querySelector('.user-name-modern')?.textContent.toLowerCase() || '';
            const userEmail = row.querySelector('.user-email-modern')?.textContent.toLowerCase() || '';
            const userPhone = row.querySelector('.contact-info-modern')?.textContent.toLowerCase() || '';
            const userRole = row.dataset.userRole;
            
            // Verificar búsqueda
            const matchesSearch = !searchTerm || 
                userName.includes(searchTerm) || 
                userEmail.includes(searchTerm) || 
                userPhone.includes(searchTerm);
            
            // Verificar filtro de rol
            const matchesFilter = filter === 'all' || userRole === filter;
            
            // Mostrar u ocultar fila
            if (matchesSearch && matchesFilter) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
        
        // Verificar si hay resultados
        const visibleRows = Array.from(tableRows).filter(row => row.style.display !== 'none');
        const tbody = document.getElementById('usersTableBody');
        
        // Eliminar mensaje de "no hay resultados" si existe
        const noResultsRow = tbody.querySelector('.no-results-row');
        if (noResultsRow) {
            noResultsRow.remove();
        }
        
        // Mostrar mensaje si no hay resultados
        if (visibleRows.length === 0) {
            const tr = document.createElement('tr');
            tr.className = 'no-results-row';
            tr.innerHTML = `
                <td colspan="6" class="text-center" style="padding: 3rem;">
                    <div class="empty-state-modern">
                        <i class="fa-solid fa-search" style="font-size: 3rem; color: #D1D5DB; margin-bottom: 1rem;"></i>
                        <p style="color: #6B7280; font-size: 1.1rem;">No se encontraron usuarios</p>
                        <p style="color: #9CA3AF; font-size: 0.9rem;">Intenta con otros términos de búsqueda o filtros</p>
                    </div>
                </td>
            `;
            tbody.appendChild(tr);
        }
    }
});
