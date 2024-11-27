import requests
from bs4 import BeautifulSoup
from colorama import Fore


def auto_gdork(query):
    """
    Automatically enhance the query with GDork operators based on keywords.

    Args:
        query (str): The user's search query.

    Returns:
        str: The enhanced query with GDork operators.
    """
    dork_keywords = {
        "site:": lambda q: f"site:{q.split()[0]} {q[len(q.split()[0]):].strip()}",
        "intitle:": lambda q: f'intitle:"{q}"',
        "inurl:": lambda q: f'inurl:"{q}"',
        "filetype:": lambda q: f'filetype:{q.split()[-1]} "{q}"',
        "related:": lambda q: f"related:{q.split()[0]}",
    }

    # Check for specific GDork patterns and apply enhancement
    for key, func in dork_keywords.items():
        if key in query:
            return func(query.replace(key, "").strip())

    # Add default GDork for basic enhancement
    return f'intext:"{query}"'


def google_search(query):
    """
    Perform a Google search with auto-detected GDork operators.

    Args:
        query (str): The search query.

    Returns:
        list: A list of search results containing title, link, and snippet.
    """
    print(Fore.CYAN + "\n[+] Performing Google Search")
    enhanced_query = auto_gdork(query)
    print(Fore.GREEN + f"Enhanced Query: {enhanced_query}")

    url = f"https://www.google.com/search?q={enhanced_query.replace(' ', '+')}"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        for g in soup.find_all("div", class_="tF2Cxc"):
            title = g.find("h3").text if g.find("h3") else "No title"
            link = g.find("a", href=True)["href"] if g.find("a", href=True) else "No link"
            snippet = (
                g.find("span", class_="aCOpRe").text
                if g.find("span", class_="aCOpRe")
                else "No description"
            )
            results.append([title, link, snippet])

        return results if results else [["No results found.", "N/A", "N/A"]]
    except Exception as e:
        return [["Error occurred", str(e), "N/A"]]

