from jina import Client
import numpy as np

async def calculate_similarity():
    client = Client(host="https://api.jina.ai/v1/embeddings")

    # Inputs
    text_description = "유전자 발현 데이터 클러스터링"
    image_base64 = ""  # Replace with actual base64 data of Monalisa painting

    # Request payload
    payload = {
        "model": "jina-clip-v2",
        "input": [
            {"text": text_description},
            {"image": image_base64}
        ]
    }

    # Send request
    response = await client.post("/v1/embeddings", json=payload)

    # Extract embeddings
    text_embedding = np.array(response.json()["data"][0]["embedding"])
    image_embedding = np.array(response.json()["data"][1]["embedding"])

    # Calculate cosine similarity (dot product of normalized vectors)
    similarity = float(np.dot(text_embedding, image_embedding))
    print(f"Similarity Score: {similarity:.4f}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(calculate_similarity())