import requests


class SearchEngine:

    def search_wikipedia(self, query: str):
        if not query:
            return None

        formatted_query = query.strip().replace(" ", "_")

        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted_query}"

        try:
            response = requests.get(url, timeout=3)

            if response.status_code != 200:
                return "No results found."

            data = response.json()

            return f"{data.get('title')}: {data.get('extract')}"

        except requests.RequestException:
            return "Search failed."