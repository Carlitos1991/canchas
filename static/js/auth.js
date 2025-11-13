document.addEventListener('DOMContentLoaded', function() {

    const container = document.getElementById('auth-container');

    // --- Botones para la vista de Escritorio (Desktop) ---
    const signUpButton = document.getElementById('signUpButton');
    const signInButton = document.getElementById('signInButton');

    // --- Botones para la vista Móvil ---
    const mobileSignUpButton = document.getElementById('mobileSignUpButton');
    const mobileSignInButton = document.getElementById('mobileSignInButton');

    // --- Lógica para cambiar de panel ---

    if (signUpButton && signInButton) {
        signUpButton.addEventListener('click', (e) => {
            e.preventDefault();
            container.classList.add('right-panel-active');
        });

        signInButton.addEventListener('click', (e) => {
            e.preventDefault();
            container.classList.remove('right-panel-active');
        });
    }

    if (mobileSignUpButton && mobileSignInButton) {
        mobileSignUpButton.addEventListener('click', (e) => {
            e.preventDefault();
            container.classList.add('right-panel-active');
        });

        mobileSignInButton.addEventListener('click', (e) => {
            e.preventDefault();
            container.classList.remove('right-panel-active');
        });
    }

    // --- Lógica para mostrar/ocultar contraseña (sin cambios) ---
    const passwordWrappers = document.querySelectorAll('.form-field-wrapper');
    passwordWrappers.forEach(wrapper => {
        const passwordInput = wrapper.querySelector('input[type="password"]');
        if (passwordInput) {
            const icon = document.createElement('i');
            icon.classList.add('fas', 'fa-eye-slash', 'password-toggle-icon');
            icon.style.cursor = 'pointer';
            wrapper.appendChild(icon);

            icon.addEventListener('click', function() {
                const isPassword = passwordInput.getAttribute('type') === 'password';
                if (isPassword) {
                    passwordInput.setAttribute('type', 'text');
                    this.classList.replace('fa-eye-slash', 'fa-eye');
                } else {
                    passwordInput.setAttribute('type', 'password');
                    this.classList.replace('fa-eye', 'fa-eye-slash');
                }
            });
        }
    });
});