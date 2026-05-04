import os
import requests
from dotenv import load_dotenv
from brain.personality import get_personality_prompt

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


class OpenRouterAI:
    def generate_response(self, prompt):
        try:
            url = "https://openrouter.ai/api/v1/chat/completions"

            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }

            # -------------------------
            # REQUEST PAYLOAD
            # -------------------------
            data = {
                # 🔥 Better model (less assistant-like)
                "model": "meta-llama/llama-3-8b-instruct",

                # 🔥 Makes responses less robotic
                "temperature": 0.8,

                "messages": [
                    {
                        "role": "system",
                        "content": get_personality_prompt()
                    },
                    {
                        "role": "user",
                        "content": f"""
Continue the conversation naturally.

User:
{prompt}
"""
                    }
                ]
            }

            # -------------------------
            # API CALL
            # -------------------------
            res = requests.post(url, headers=headers, json=data)

            if res.status_code == 200:
                text = res.json()["choices"][0]["message"]["content"]

                return {
                    "text": text.strip(),
                    "source": "openrouter",
                    "status": "success"
                }
            else:
                print(f"⚠️ OpenRouter Status: {res.status_code}")
                print(res.text)

        except Exception as e:
            print(f"⚠️ OpenRouter error: {e}")

        return {
            "text": "Something went wrong while contacting OpenRouter.",
            "source": "openrouter",
            "status": "fail"
        }