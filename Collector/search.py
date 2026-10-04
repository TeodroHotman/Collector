import requests

SEARXNG_URL = "http://127.0.0.1:8888/search"  # Replace with real SearXNG instance URL

def search_source(websites, keywords, topics):
    results = []
    queries = []
    
    for keyword in keywords:
        for topic in topics:
            queries.append(f"{keyword} {topic}")

    for query in queries:
        if websites:
            searches = [
            f"site: {website} {query}" 
            for website in websites
            ]
        else:
            searches = [query]

        for search_query in searches:
            params = {
        "q": search_query,
        "format": "json"
        }

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(SEARXNG_URL, params=params, headers=headers, timeout=10)

    print("STATUS:", response.status_code)
    print("CONTENT TYPE:", response.headers.get("content-type"))
    print("QUERY:", search_query)

    response.raise_for_status()
    data = response.json()

    for result in data.get("results", []):
        url = result.get("url", "")
        if url:
            source = url.split("/")[2].replace("www.", "")
        else:
            source = ""
        results.append({
            "title": result.get("url", ""),
            "url": url,
            "source": url.split("/")[2] if url else "",
            "preview": result.get("content", ""),
            "engine": result.get("engine", ""),
            "query": query
        })
    return results