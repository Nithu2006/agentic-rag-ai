from typing import List, Dict

import requests
from bs4 import BeautifulSoup


def search_web(
    query: str,
    max_results: int = 5,
) -> List[Dict]:
    """
    Search the web using DuckDuckGo HTML search.
    No API key is required.
    """

    url = "https://html.duckduckgo.com/html/"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/153.0 Safari/537.36"
        )
    }

    try:

        response = requests.post(
            url,
            data={"q": query},
            headers=headers,
            timeout=10,
        )

        response.raise_for_status()

    except requests.RequestException as error:

        print(
            f"Web search failed: {error}"
        )

        return []

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    results = []

    for result in soup.select(
        ".result"
    )[:max_results]:

        title_element = result.select_one(
            ".result__title"
        )

        link_element = result.select_one(
            ".result__a"
        )

        snippet_element = result.select_one(
            ".result__snippet"
        )

        if not link_element:
            continue

        title = (
            title_element.get_text(
                " ",
                strip=True
            )
            if title_element
            else "Web Result"
        )

        link = link_element.get(
            "href",
            ""
        )

        snippet = (
            snippet_element.get_text(
                " ",
                strip=True
            )
            if snippet_element
            else ""
        )

        results.append(
            {
                "title": title,
                "url": link,
                "snippet": snippet,
                "source": "web",
            }
        )

    return results


def run_web_search(
    query: str,
) -> Dict:
    """
    Run the Web Search Agent.
    This function is used by the orchestrator.
    """

    results = search_web(
        query=query,
        max_results=5,
    )

    return {
        "query": query,
        "results": results,
        "source": "web",
        "success": len(results) > 0,
    }