export async function apiFetch(url, options = {}) {
    const resp = await fetch(url, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {})
        },
        credentials: "include"
    });

    const data = await resp.json().catch(() => ({}));

    // Access token expired → try refresh
    if (resp.status === 401 && data.error === "token_expired") {
        const refreshed = await fetch("/refresh", {
            method: "POST",
            credentials: "include"
        });

        if (refreshed.ok) {
            return fetch(url, {
                ...options,
                headers: {
                    "Content-Type": "application/json",
                    ...(options.headers || {})
                },
                credentials: "include"
            });
        } else {
            showLoginModal();
            throw new Error("Login required");
        }
    }

    // Refresh token expired -> force login
    if (resp.status === 403) {
        showLoginModal();
        throw new Error("Login required");
    }

    // Any other error -> show inline
    if (!resp.ok) {
        throw new Error(data.error || "Request failed");
    }

    return data;
}

function showLoginModal() {
    const modal = document.getElementById("choiceModal");
    const body = document.body;
    if (modal) {
        modal.classList.add("open");
        body.classList.add("modal-open");
    }
}
