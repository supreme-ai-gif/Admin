const BASE_URL = "https://genetic-ai.onrender.com";

// ---------------------
// Create API Key
// ---------------------
async function createKey() {
    const owner = document.getElementById("owner").value;
    const password = document.getElementById("password").value;

    const formData = new FormData();
    formData.append("owner", owner);
    formData.append("password", password);

    let resultText = document.getElementById("createResult");

    try {
        const res = await fetch(`${BASE_URL}/admin/create_key`, {
            method: "POST",
            body: formData
        });

        const data = await res.json();
        if (data.key) {
            resultText.innerText = "API Key Created: " + data.key;
        } else {
            resultText.innerText = "Error: " + JSON.stringify(data);
        }
    } catch (err) {
        resultText.innerText = "Request Failed";
    }
}

// ---------------------
// List All Keys
// ---------------------
async function listKeys() {
    const password = document.getElementById("passwordList").value;
    let out = document.getElementById("keysOutput");

    try {
        const res = await fetch(`${BASE_URL}/admin/list_keys?password=${password}`);
        const data = await res.json();

        if (data.keys) {
            out.innerText = JSON.stringify(data.keys, null, 2);
        } else {
            out.innerText = "Error: " + JSON.stringify(data);
        }
    } catch (err) {
        out.innerText = "Failed to fetch keys.";
    }
}

// ---------------------
// Revoke API Key
// ---------------------
async function revokeKey() {
    const key = document.getElementById("keyToRevoke").value;
    const password = document.getElementById("passwordRevoke").value;

    const formData = new FormData();
    formData.append("key", key);
    formData.append("password", password);

    let out = document.getElementById("revokeResult");

    try {
        const res = await fetch(`${BASE_URL}/admin/revoke_key`, {
            method: "POST",
            body: formData
        });

        const data = await res.json();
        out.innerText = data.success ? "Key Revoked!" : "Key Not Found";
    } catch (err) {
        out.innerText = "Failed request.";
    }
}
