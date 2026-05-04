from core.search_engine import SearchEngine


class TaskEngine:

    def __init__(self):
        self.search_engine = SearchEngine()

    def detect_intent(self, prompt: str):
        p = prompt.lower()

        if p.startswith("search "):
            return "search"

        return "none"

    def extract_query(self, prompt: str):
        return prompt[7:].strip()  # removes "search "

    def handle(self, prompt: str):

        intent = self.detect_intent(prompt)

        if intent == "search":
            query = self.extract_query(prompt)

            if not query:
                return None

            return self.search_engine.search_wikipedia(query)

        return None