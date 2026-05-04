from brain.manager import BrainManager

brain = BrainManager()


def ask_ai(prompt: str) -> dict:
    try:
        return brain.ask(prompt)
    except Exception as e:
        return {
            "text": f"AI Error: {str(e)}",
            "source": "error",
            "status": "fail"
        }