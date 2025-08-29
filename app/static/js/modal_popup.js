import { register, login } from "./jwt_auth.js";

document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('choiceModal');
    const body = document.body;
    const closeModal = document.getElementById('closeModal');
    const getStartedBtn = document.getElementById('getStartedBtn');

    if (getStartedBtn) {
        getStartedBtn.addEventListener('click', () => {
            modal.classList.add('open');
            modal.classList.add('modal-open');
        })
    }

    if (closeModal) {
        closeModal.addEventListener('click', () => {
            modal.classList.remove('open');
            body.classList.remove('modal-open');
        });
    }

        // Toggle password
    document.getElementById("togglePassword").addEventListener("click", function () {
        const pwdInput = document.getElementById("passwordInput");
        const img = this.querySelector("img");
        const eyeOpen = this.dataset.eyeOpen;
        const eyeClosed = this.dataset.eyeClosed;

        if (pwdInput.type === "password") {
            pwdInput.type = "text";
            img.src = eyeOpen;
        } else {
            pwdInput.type = "password";
            img.src = eyeClosed;
        }
    });

   // Handle register/login buttons
    const registerBtn = document.getElementById('registerBtn');
    const loginBtn = document.getElementById('loginBtn');
    const emailInput = document.getElementById('emailInput');
    const passwordInput = document.getElementById('passwordInput');
    const nameInput = document.getElementById('nameInput');
    const errorMsg = document.getElementById('ErrorMessage');

    registerBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        errorMsg.style.display = "none";
        try {
            const resp = await register(emailInput.value, passwordInput.value, nameInput.value);
            if (resp.redirect) window.location.href = resp.redirect;   
        } catch (err) {
            errorMsg.textContent = " ! " + err.message;
            errorMsg.style.display = "block";
        }
    });

    loginBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        errorMsg.style.display = "none";
        try {
            const resp = await login(emailInput.value, passwordInput.value);
            if (resp.redirect) window.location.href = resp.redirect;
        } catch (err) {
            errorMsg.textContent = " ! " + err.message;
            errorMsg.style.display = "block";
        }
    });
});
