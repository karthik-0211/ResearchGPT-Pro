# pyrefly: ignore [missing-import]
from duckduckgo_search import DDGS
import urllib.request
import urllib.parse
import json
import re

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def search_wikipedia(query, max_results=5):
    try:
        encoded_query = urllib.parse.quote(query)
        url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={encoded_query}&format=json&origin=*"
        
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
        )
        
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            search_results = data.get("query", {}).get("search", [])
            
            results = []
            for item in search_results[:max_results]:
                title = item.get("title", "")
                snippet = clean_html(item.get("snippet", ""))
                pageid = item.get("pageid", "")
                url = f"https://en.wikipedia.org/?curid={pageid}"
                
                results.append({
                    "title": f"Wikipedia: {title}",
                    "content": snippet + "...",
                    "url": url
                })
            return results
    except Exception as e:
        print("Wikipedia Search Error:", e)
        return []

def search_web(query, max_results=8):
    results = []

    try:
        with DDGS() as ddgs:
            response = ddgs.text(
                query,
                max_results=max_results
            )

            for item in response:
                results.append({
                    "title": item.get("title", ""),
                    "content": item.get("body", ""),
                    "url": item.get("href", "")
                })

        # Fallback to news search if web search yielded no results
        if not results:
            print("Web search returned no results. Trying news fallback...")
            with DDGS() as ddgs:
                response = ddgs.news(
                    query,
                    max_results=max_results
                )

                for item in response:
                    results.append({
                        "title": item.get("title", ""),
                        "content": item.get("body", ""),
                        "url": item.get("url", "")
                    })

    except Exception as e:
        print("Web Search Error:", e)
        try:
            print("Trying news fallback after error...")
            with DDGS() as ddgs:
                response = ddgs.news(
                    query,
                    max_results=max_results
                )

                for item in response:
                    results.append({
                        "title": item.get("title", ""),
                        "content": item.get("body", ""),
                        "url": item.get("url", "")
                    })
        except Exception as e_news:
            print("News Fallback Error:", e_news)

    # Fallback to Wikipedia search if both web and news searches returned no results
    if not results:
        print("DuckDuckGo search options failed or returned no results. Trying Wikipedia fallback...")
        results = search_wikipedia(query, max_results=max_results)

    return results
