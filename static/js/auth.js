// Espera a que todo el HTML esté cargado antes de ejecutar el script
document.addEventListener('DOMContentLoaded', function() {

    // --- Lógica de Animación de Deslizamiento ---
    const signUpButton = document.getElementById('signUpButton');
    const signInButton = document.getElementById('signInButton');
    const container = document.getElementById('auth-container');

    if (signUpButton && signInButton && container) {
        signUpButton.addEventListener('click', () => {
            container.classList.add('right-panel-active');
        });

        signInButton.addEventListener('click', () => {
            container.classList.remove('right-panel-active');
        });
    }

    // --- Lógica de Mostrar/Ocultar Contraseña ---

    // Función reutilizable
    function setupPasswordToggle(toggleId, passwordId) {
        const toggleButton = document.getElementById(toggleId);
        // Django añade 'id_' al ID del input
        const passwordInput = document.getElementById('id_' + passwordId);

        if (toggleButton && passwordInput) {
            toggleButton.addEventListener('click', function() {
                // Cambia el tipo de input
                const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
                passwordInput.setAttribute('type', type);

                // Cambia el icono
                this.classList.toggle('fa-eye');
                this.classList.toggle('fa-eye-slash');
            });
        }
    }

    // --- CAMBIO AQUÍ ---
    // Configura los 3 botones con los nuevos IDs prefijados
    setupPasswordToggle('toggle-password-login', 'login-password');
    setupPasswordToggle('toggle-password-signup', 'signup-password');
    setupPasswordToggle('toggle-password-confirm', 'signup-password_confirm');
    // --- FIN DEL CAMBIO ---

});