document.addEventListener('DOMContentLoaded', () => {
    const body = document.body;
    const sidebar = document.querySelector('.sidebar');
    const themeToggle = document.getElementById('theme-toggle-checkbox');

    // --- Lógica para Sidebar en Escritorio ---
    const sidebarToggle = document.getElementById('sidebar-toggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', (event) => {
            event.preventDefault();
            // CORRECCIÓN: Solo colapsar en pantallas de escritorio
            if (window.innerWidth > 768) {
                sidebar.classList.toggle('collapsed');
                localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
            }
        });
    }

    // --- Lógica para Sidebar en Móvil ---
    const mobileSidebarToggle = document.getElementById('mobile-sidebar-toggle');
    const sidebarOverlay = document.querySelector('.sidebar-overlay');

    if (mobileSidebarToggle && sidebarOverlay) {
        // Abrir sidebar
        mobileSidebarToggle.addEventListener('click', () => {
            body.classList.add('sidebar-open');
        });

        // Cerrar sidebar con el overlay
        sidebarOverlay.addEventListener('click', () => {
            body.classList.remove('sidebar-open');
        });
    }

    // --- Lógica para Modo Oscuro ---
    if (themeToggle) {
        themeToggle.addEventListener('change', () => {
            body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', body.classList.contains('dark-mode'));
        });
    }

    // --- Cargar preferencias guardadas al iniciar ---
    if (window.innerWidth > 768) {
        const isSidebarCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
        if (isSidebarCollapsed) {
            sidebar.classList.add('collapsed');
        }
    }

    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    if (isDarkMode) {
        body.classList.add('dark-mode');
        if (themeToggle) {
            themeToggle.checked = true;
        }
    }
});