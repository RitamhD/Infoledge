import { apiFetch } from "./api.js";

export async function register(email, password, name) {
    const result = apiFetch("/register", {
        method: "POST",
        body: JSON.stringify({email, password, name})
    });
    startScheduledRefresh(25);
    return result;
}

export async function login(email, password) {
    const result = apiFetch("/login", {
        method: "POST",
        body: JSON.stringify({email, password})
    });
    startScheduledRefresh(25);
    return result;
}

export async function logout() {
    return apiFetch("/logout", {
        method: "POST"
    });
}

let refreshIntervalId;
export function startScheduledRefresh(interval = 25) {
    if (refreshIntervalId) return;  //already refresh running

    refreshIntervalId = setInterval(async () => {
        await fetch ("/refresh", {
            method: "POST",
            credentials: "include"
        });
    }, interval * 60 * 1000);
}