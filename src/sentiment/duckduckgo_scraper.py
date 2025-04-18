import requests
from bs4 import BeautifulSoup

def search_duckduckgo(query, num_results=10):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    params = {
        "q": f"{query} crypto",
        "kl": "us-en"
    }

    response = requests.get("https://html.duckduckgo.com/html/", params=params, headers=headers)
    if response.status_code != 200:
        print(f"DuckDuckGo request failed: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for result in soup.select("div.result__body")[:num_results]:
        title = result.select_one(".result__title").get_text(strip=True)
        snippet = result.select_one(".result__snippet")
        snippet_text = snippet.get_text(strip=True) if snippet else ""
        results.append({
            "title": title,
            "snippet": snippet_text
        })

    return results
