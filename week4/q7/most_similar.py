import numpy as np

def most_similar(embeddings):
    def cosine_similarity(vec1, vec2):
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    phrases = list(embeddings.keys())
    max_similarity = -1
    most_similar_pair = (None, None)

    for i in range(len(phrases)):
        for j in range(i + 1, len(phrases)):
            phrase1, phrase2 = phrases[i], phrases[j]
            similarity = cosine_similarity(embeddings[phrase1], embeddings[phrase2])
            if similarity > max_similarity:
                max_similarity = similarity
                most_similar_pair = (phrase1, phrase2)

    return most_similar_pair