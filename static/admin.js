// admin.js

const AI_SERVER_URL = "https://genetic-ai.onrender.com"; // Replace with your AI server URL
const MASTER_PASSWORD = prompt("Enter master password for AI server:");

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("create-key-form");
    if (form) {
        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            const owner = form.owner.value;

            const res = await fetch(`${AI_SERVER_URL}/admin/create_key`, {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: new URLSearchParams({ owner: owner, password: MASTER_PASSWORD })
            });

            const data = await res.json();
            if (data.success) {
                alert("API Key created: " + data.key);
                location.reload();
            } else {
                alert("Failed to create key");
            }
        });
    }
});

async function revokeKey(key) {
    const res = await fetch(`${AI_SERVER_URL}/admin/revoke_key`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ key: key, password: MASTER_PASSWORD })
    });

    const data = await res.json();
    if (data.success) {
        alert("Key revoked");
        location.reload();
    } else {
        alert("Failed to revoke key");
    }
}
