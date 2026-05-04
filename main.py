from brain.manager import BrainManager
from brain.personality import set_personality, get_personality
import socket
import os
import json
from datetime import datetime


# -------------------------
# NETWORK CHECK
# -------------------------
def is_online():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False


# -------------------------
# SESSION STORAGE (GREETING)
# -------------------------
SESSION_FILE = "core/session.json"


def load_session():
    if not os.path.exists(SESSION_FILE):
        return {"last_greet_date": ""}

    with open(SESSION_FILE, "r") as f:
        return json.load(f)


def save_session(data):
    with open(SESSION_FILE, "w") as f:
        json.dump(data, f)


# -------------------------
# MAIN
# -------------------------
def main():
    brain = BrainManager()

    status = "ONLINE" if is_online() else "OFFLINE"
    print(f"[LECH SYSTEM] Boot complete → {status}")
    print("Active: JARVIS (default)")
    print("Commands: /jarvis, /sadie, /clear, exit\n")

    session = load_session()
    today = datetime.now().strftime("%Y-%m-%d")

    while True:

        # -------------------------
        # JARVIS GREETING (ONCE PER DAY ONLY)
        # -------------------------
        if session.get("last_greet_date") != today:

            persona = get_personality()

            if persona == "jarvis":
                greet_prompt = (
                    "Greet as JARVIS.\n"
                    "- ONE short sentence\n"
                    "- Offer updates in AI/QA/tech\n"
                )

                response = brain.ask(greet_prompt)
                text = response.get("text") if isinstance(response, dict) else response

                if text:
                    print(f"\n[JARVIS]: {text}\n")

            # Save once
            session["last_greet_date"] = today
            save_session(session)

        # -------------------------
        # INPUT
        # -------------------------
        user_input = input(">> ").strip()

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("[LECH SYSTEM] Shutdown")
            break

        # -------------------------
        # CLEAR SCREEN
        # -------------------------
        if user_input == "/clear":
            os.system("cls" if os.name == "nt" else "clear")
            continue

        # -------------------------
        # SWITCH → JARVIS
        # -------------------------
        if user_input == "/jarvis":
            set_personality("jarvis")
            print("[LECH SYSTEM] Switched → JARVIS\n")
            continue

        # -------------------------
        # SWITCH → SADIE (WITH NATURAL START)
        # -------------------------
        if user_input == "/sadie":
            set_personality("sadie")
            print("[LECH SYSTEM] Switched → Sadie\n")

            prompt = (
                "Start a natural human conversation.\n"
                "- No greeting like hello\n"
                "- No formal tone\n"
                "- Just a casual opening line\n"
            )

            response = brain.ask(prompt)
            text = response.get("text") if isinstance(response, dict) else response

            if text:
                print(f"[Sadie]: {text}\n")

            continue

        # -------------------------
        # NORMAL FLOW
        # -------------------------
        response = brain.ask(user_input)

        persona = get_personality()
        name = "JARVIS" if persona == "jarvis" else "Sadie"

        text = None
        if isinstance(response, dict):
            text = response.get("text")
        else:
            text = response

        if not text:
            print(f"\n[{name}]: I couldn't process that properly.\n")
        else:
            print(f"\n[{name}]: {text}\n")


# -------------------------
# ENTRY
# -------------------------
if __name__ == "__main__":
    main()