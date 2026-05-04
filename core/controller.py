from brain.manager import BrainManager

brain = BrainManager()


def process_input(user_input, system_state):
    if not system_state["is_active"]:
        return "AI not active"

    response = brain.ask(user_input)
    return response["text"]