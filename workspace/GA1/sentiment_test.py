import httpx

url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Authorization": "Bearer DUMMY_API_KEY",
    "Content-Type": "application/json",
}
payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {
            "role": "system",
            "content": "Analyze the sentiment of the provided text and classify it into exactly one of the categories: GOOD, BAD, or NEUTRAL. Respond with the category and a one-line justification."
        },
        {
            "role": "user",
            "content": "WaDOa LECgLabe0 hg 7JhUo qa f43PP LfoQ5uKg8r8JT ON"
        }
    ],
    "max_tokens": 60,
}

response = httpx.post(url, json=payload, headers=headers)
response.raise_for_status()
print(response.json())