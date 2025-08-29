export function startScheduledRefresh(interval = 25) {
    setInterval(async () => {
        await fetch ("/refresh", {
            method: "POST",
            credentials: "include"
        });
    }, interval * 60 * 1000);
}