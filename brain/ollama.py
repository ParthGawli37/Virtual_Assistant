import subprocess


class OllamaAI:
    def generate_response(self, prompt):
        try:
            result = subprocess.run(
                ["ollama", "run", "mistral"],
                input=prompt,
                capture_output=True,
                text=True,
                encoding="utf-8"  # ✅ ADD THIS
            )

            return {
                "text": result.stdout.strip().replace("\n", " "),
                "source": "ollama",
                "status": "success"
            }

        except Exception as e:
            print(f"⚠️ Ollama failed: {e}")
            return {"status": "fail"}