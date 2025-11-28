document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.querySelector('.sidebar');
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const themeToggle = document.getElementById('theme-toggle-checkbox');
    const body = document.body;
    const isMobile = window.innerWidth <= 768;

    // --- 1. LÓGICA DEL SIDEBAR (COLLAPSE) ---
    // (Esta parte ya la tenías, solo confirma que sidebarToggle existe)
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', () => {
            if (window.innerWidth <= 768) {
                sidebar.classList.toggle('mobile-active');
            } else {
                sidebar.classList.toggle('collapsed');
                // Guardar preferencia
                localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
            }
        });
    }

    // Cargar preferencia guardada (solo escritorio)
    if (!isMobile && localStorage.getItem('sidebarCollapsed') === 'true') {
        sidebar.classList.add('collapsed');
    }

    // --- 2. LÓGICA DEL DROPDOWN DE USUARIO (NUEVO) ---
    const dropdownTrigger = document.getElementById('dropdownTrigger');
    const dropdownMenu = document.getElementById('dropdownMenu');

    if (dropdownTrigger && dropdownMenu) {
        // Toggle al hacer click
        dropdownTrigger.addEventListener('click', (e) => {
            e.stopPropagation(); // Evita burbujeo inmediato
            dropdownMenu.classList.toggle('show');
        });

        // Cerrar al hacer click fuera
        document.addEventListener('click', (e) => {
            if (!dropdownMenu.contains(e.target) && !dropdownTrigger.contains(e.target)) {
                dropdownMenu.classList.remove('show');
            }
        });
    }

    // --- 3. MODO OSCURO ---
    // (Igual que antes)
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    if (isDarkMode) {
        body.classList.add('dark-mode');
        if (themeToggle) themeToggle.checked = true;
    }
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', body.classList.contains('dark-mode'));
        });
    }

    // --- 4. CIERRE MÓVIL ---
    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 768 &&
            sidebar.classList.contains('mobile-active') &&
            !sidebar.contains(e.target) &&
            e.target !== sidebarToggle &&
            !sidebarToggle.contains(e.target)) {
            sidebar.classList.remove('mobile-active');
        }
    });
});