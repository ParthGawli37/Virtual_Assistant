import requests


class WorldEngine:

    # -------------------------
    # WEATHER (Open-Meteo)
    # -------------------------
    def get_weather(self, city="Mumbai"):
        try:
            coords = {
                "Mumbai": (19.0760, 72.8777),
                "Delhi": (28.7041, 77.1025),
                "Bangalore": (12.9716, 77.5946)
            }

            lat, lon = coords.get(city, (19.0760, 72.8777))

            url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={lat}&longitude={lon}&current_weather=true"
            )

            response = requests.get(url, timeout=3)

            if response.status_code != 200:
                return self._fallback()

            data = response.json()
            current = data.get("current_weather", {})

            temp = current.get("temperature")
            wind = current.get("windspeed")

            feel = self._get_feel(temp)

            return {
                "temperature": temp,
                "wind": wind,
                "feel": feel
            }

        except requests.RequestException:
            return self._fallback()

    # -------------------------
    # TREND SIGNAL (STATIC)
    # -------------------------
    def get_trend_signal(self):
        return {
            "topics": [
                "AI",
                "automation tools",
                "tech layoffs",
                "cricket"
            ]
        }

    # -------------------------
    # COMBINED CONTEXT
    # -------------------------
    def get_world_context(self):
        return {
            "weather": self.get_weather(),
            "trends": self.get_trend_signal()
        }

    # -------------------------
    # HELPERS
    # -------------------------
    def _get_feel(self, temp):
        if temp is None:
            return "unknown"
        if temp > 32:
            return "hot"
        if temp < 18:
            return "cool"
        return "neutral"

    def _fallback(self):
        return {
            "temperature": None,
            "wind": None,
            "feel": "unknown"
        }