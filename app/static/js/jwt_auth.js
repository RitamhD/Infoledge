import { apiFetch } from "./api.js";

export async function register(email, password, name) {
    return apiFetch("/register", {
        method: "POST",
        body: JSON.stringify({email, password, name})
    });
}

export async function login(email, password) {
    return apiFetch("/login", {
        method: "POST",
        body: JSON.stringify({email, password})
    });
}

export async function logout() {
    return apiFetch("/logout", {
        method: "POST"
    });
}
