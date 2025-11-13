document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.querySelector('.sidebar');
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const themeToggle = document.getElementById('theme-toggle-checkbox'); // Corregido para apuntar al checkbox
    const body = document.body;

    // --- 1. Cargar preferencias guardadas al iniciar ---

    // Cargar estado del sidebar
    const isSidebarCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
    if (isSidebarCollapsed) {
        sidebar.classList.add('collapsed');
    }

    // Cargar estado del modo oscuro
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    if (isDarkMode) {
        body.classList.add('dark-mode');
        if (themeToggle) {
            themeToggle.checked = true;
        }
    }

    // --- 2. Event Listener para el Sidebar ---
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
            // Guardar la preferencia
            localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
        });
    }

    // --- 3. Event Listener para el Modo Oscuro ---
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            body.classList.toggle('dark-mode');
            // Guardar la preferencia
            localStorage.setItem('darkMode', body.classList.contains('dark-mode'));
        });
    }
});