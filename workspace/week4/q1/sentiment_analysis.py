import httpx

def analyze_sentiment():
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer dummy_api_key"
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Analyze the sentiment of the text into GOOD, BAD, or NEUTRAL."},
            {"role": "user", "content": "WaDOa LECgLabe0 hg 7JhUo qa f43PP LfoQ5uKg8r8JT ON"}
        ]
    }

    try:
        response = httpx.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        print("Sentiment Analysis Result:", result)
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    analyze_sentiment()