import openai

def calculate_token_usage():
    openai.api_key = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIyZjMwMDI1NzlAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.quZ6q8sX_ne0Gcu2QCl9cJtHv8CK2CoJ7OiXSSBWmQs"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "List only the valid English words from these: QCbzYK0IOf, yOqze, F, N, VYlyeMUZ, iUPk4iI, H9, P9mKak, aU2jmOeMu, WMiZg0, RQK763Y, NkL3T, 4, fmGEnTD1, OlJIGUe, C7Fb04e7, CBmIb7T, p6oyGpRVF, heJf5, WNfN9f, HZq3hdF, zX, jq, gXU12Te, QH6W, iI2yuO4GJK, 1l, cwSEtn, xLfYm, 1rtBXPm, 1UL, 9rYu0fhTl, L75QD, f0qtL, p1, nJZ2VwZqo7, d9H, evqKZ1ckf, y, 8UAQKU4z, 7Lx, utKIlZeZ2, t, fCKjlXW3, U2, mXUGuMv, P, 2qmHhoD, 2ld4xA1Y, M6r, YyLrcwpmPY, Sko9pQlIXN, I0cEo2, ZP9OE, wJxeX2Dbo, aakmmXt, y, Se9sA, Pi, SbDtS, d, wqpzVhx, FuW, Lnx, m, VQJP8wWr, 2WO, Y6aho, QwH, 5NgwuCMoAr, oBGw, 1b, sM5tC1, 5dqE8P"}
            ]
        )

        print("Number of tokens used:", response["usage"]["total_tokens"])
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    calculate_token_usage()