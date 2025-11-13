/*
Este script maneja dos (2) funcionalidades en la página de login/registro:
1. La animación de deslizamiento (Slider) entre los paneles de "Sign In" y "Sign Up".
2. La lógica para mostrar/ocultar la contraseña (Password Toggle).
*/

// Esperamos a que todo el contenido del HTML esté cargado antes de ejecutar el script.
document.addEventListener('DOMContentLoaded', () => {

    /* --- 1. LÓGICA DE LA ANIMACIÓN (SLIDER) --- */

    // Obtenemos los botones y el contenedor principal por sus IDs del HTML
    const signUpButton = document.getElementById('signUpButton');
    const signInButton = document.getElementById('signInButton');
    const container = document.getElementById('auth-container');

    // Añadimos un 'event listener' al botón "Registrarse"
    if (signUpButton) {
        signUpButton.addEventListener('click', () => {
            // Añadimos la clase que activa la animación en el CSS
            container.classList.add('right-panel-active');
        });
    }

    // Añadimos un 'event listener' al botón "Iniciar Sesión"
    if (signInButton) {
        signInButton.addEventListener('click', () => {
            // Quitamos la clase para revertir la animación
            container.classList.remove('right-panel-active');
        });
    }

    /* --- 2. LÓGICA DE MOSTRAR/OCULTAR CONTRASEÑA --- */

    /**
     * Función reutilizable para alternar la visibilidad de un campo de contraseña.
     * @param {string} toggleButtonId - El ID del botón (el icono del "ojo").
     * @param {string} passwordFieldId - El ID del campo de contraseña (input).
     */
    const setupPasswordToggle = (toggleButtonId, passwordFieldId) => {
        const toggleButton = document.getElementById(toggleButtonId);
        const passwordField = document.getElementById(passwordFieldId);

        // Nos aseguramos de que ambos elementos existan antes de añadir el listener
        if (toggleButton && passwordField) {
            toggleButton.addEventListener('click', () => {
                // Cambiamos el 'type' del input
                const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
                passwordField.setAttribute('type', type);

                // Cambiamos el icono del "ojo"
                toggleButton.classList.toggle('fa-eye');
                toggleButton.classList.toggle('fa-eye-slash');
            });
        }
    };

    // --- Configuramos los 3 botones de contraseña ---
    // Usamos los IDs que Django genera con los prefijos (ej. 'id_login-password')

    // 1. Para el formulario de Login
    setupPasswordToggle('toggle-password-login', 'id_login-password');

    // 2. Para el formulario de Registro (Contraseña)
    setupPasswordToggle('toggle-password-signup', 'id_signup-password');

    // 3. Para el formulario de Registro (Confirmar Contraseña)
    setupPasswordToggle('toggle-password-confirm', 'id_signup-password_confirm');

});