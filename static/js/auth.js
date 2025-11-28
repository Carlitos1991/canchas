/* static/js/auth.js */

// Función Global para alternar contraseña
window.togglePassword = function(inputId, iconId) {
    const input = document.getElementById(inputId);
    const icon = document.getElementById(iconId);

    if (input && icon) {
        const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
        input.setAttribute('type', type);

        // Alternar icono
        if (type === 'text') {
            icon.classList.remove('fa-eye');
            icon.classList.add('fa-eye-slash');
        } else {
            icon.classList.remove('fa-eye-slash');
            icon.classList.add('fa-eye');
        }
    } else {
        console.error("Error: No se encontró el input o el icono");
    }
}

// Lógica del Slider (Se mantiene igual)
document.addEventListener('DOMContentLoaded', () => {
    const signUpButton = document.getElementById('signUpButton');
    const signInButton = document.getElementById('signInButton');
    const container = document.getElementById('auth-container');

    if (signUpButton && container) {
        signUpButton.addEventListener('click', () => {
            container.classList.add('right-panel-active');
        });
    }

    if (signInButton && container) {
        signInButton.addEventListener('click', () => {
            container.classList.remove('right-panel-active');
        });
    }
});