import { getProfile } from "https://aipipe.org/aipipe.js";

async function calculateTokenUsage() {
    const { token, email } = getProfile();
    if (!token) {
        window.location = `https://aipipe.org/login?redirect=${window.location.href}`;
        return;
    }

    try {
        const response = await fetch("https://aipipe.org/openrouter/v1/responses", {
            method: "POST",
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                model: "openai/gpt-4.1-nano",
                input: "What is 2 + 2?"
            })
        });

        const result = await response.json();
        console.log("Response Result:", result);
    } catch (error) {
        console.error("An error occurred:", error);
    }
}

calculateTokenUsage();