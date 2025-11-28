/* static/js/auth.js */

// Función Global para alternar contraseña
window.togglePassword = function(inputId, iconId) {
    const inputElement = document.getElementById(inputId);
    const iconElement = document.getElementById(iconId);

    if (inputElement && iconElement) {
        const type = inputElement.getAttribute('type') === 'password' ? 'text' : 'password';
        inputElement.setAttribute('type', type);

        // Alternar icono
        if (type === 'text') {
            iconElement.classList.remove('fa-eye');
            iconElement.classList.add('fa-eye-slash');
        } else {
            iconElement.classList.remove('fa-eye-slash');
            iconElement.classList.add('fa-eye');
        }
    }
}

// Lógica del Slider
document.addEventListener('DOMContentLoaded', () => {
    const signUpButton = document.getElementById('signUpButton');
    const signInButton = document.getElementById('signInButton');
    const mobileSignUp = document.getElementById('mobileSignUp');
    const mobileSignIn = document.getElementById('mobileSignIn');
    const container = document.getElementById('auth-container');

    // Desktop - Botones del overlay
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

    // Mobile - Enlaces de cambio
    if (mobileSignUp && container) {
        mobileSignUp.addEventListener('click', (e) => {
            e.preventDefault();
            container.classList.add('right-panel-active');
        });
    }

    if (mobileSignIn && container) {
        mobileSignIn.addEventListener('click', (e) => {
            e.preventDefault();
            container.classList.remove('right-panel-active');
        });
    }

    // Animación de entrada suave
    setTimeout(() => {
        if (container) {
            container.style.opacity = '1';
            container.style.transform = 'scale(1)';
        }
    }, 100);

    // Mostrar errores con SweetAlert
    showErrors();
});

// Función para mostrar errores con SweetAlert
function showErrors() {
    // Errores de login
    const loginErrors = document.querySelectorAll('.sign-in-container .errorlist li, .sign-in-container .alert-error li');
    if (loginErrors.length > 0) {
        const errorMessages = Array.from(loginErrors).map(li => li.textContent.trim()).join('<br>');
        Swal.fire({
            icon: 'error',
            title: 'Error al iniciar sesión',
            html: errorMessages,
            confirmButtonText: 'Entendido',
            confirmButtonColor: '#10B981',
            customClass: {
                popup: 'auth-swal-popup'
            }
        });
    }

    // Errores de registro
    const signupErrors = document.querySelectorAll('.sign-up-container .errorlist li, .sign-up-container .alert-error li');
    if (signupErrors.length > 0) {
        const errorMessages = Array.from(signupErrors).map(li => li.textContent.trim()).join('<br>');
        Swal.fire({
            icon: 'error',
            title: 'Error al registrarse',
            html: errorMessages,
            confirmButtonText: 'Entendido',
            confirmButtonColor: '#10B981',
            customClass: {
                popup: 'auth-swal-popup'
            }
        });
    }
}

// Inicializar con animación
window.addEventListener('load', () => {
    const container = document.getElementById('auth-container');
    if (container) {
        container.style.opacity = '0';
        container.style.transform = 'scale(0.95)';
        container.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
    }
});
