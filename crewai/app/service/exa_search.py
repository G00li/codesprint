import requests
import os

EXA_API_KEY = os.getenv("EXA_API_KEY")
EXA_API_URL = "https://api.exa.ai/search"

def buscar_com_exa(query: str, num_results: int = 5) -> list[str]:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {EXA_API_KEY}"
    }

    payload = {
        "query": query,
        "numResults": num_results
    }

    response = requests.post(EXA_API_URL, json=payload, headers=headers)
    response.raise_for_status()

    results = response.json().get("results", [])
    return [r.get("text", "") for r in results]
