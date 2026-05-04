import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


class GroqAI:
    def generate_response(self, prompt):
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"

            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "llama-3.1-8b-instant",  # ✅ stable model
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }

            res = requests.post(url, headers=headers, json=data, timeout=10)

            # 🔍 DEBUG
            print("Groq Status:", res.status_code)

            if res.status_code != 200:
                print("Groq Error:", res.text)
                return {"status": "fail"}

            response_json = res.json()

            if "choices" in response_json:
                text = response_json["choices"][0]["message"]["content"]

                return {
                    "text": text.strip(),
                    "source": "groq",
                    "status": "success"
                }

        except Exception as e:
            print(f"⚠️ Groq Exception: {e}")

        return {"status": "fail"}