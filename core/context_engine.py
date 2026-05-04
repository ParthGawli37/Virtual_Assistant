import datetime
import time


class ContextEngine:

    def __init__(self):
        self.last_user_input_time = time.time()
        self.session_start_time = time.time()
        self.interaction_count = 0

    # -------------------------
    # UPDATE USER ACTIVITY
    # -------------------------
    def update_activity(self):
        self.last_user_input_time = time.time()
        self.interaction_count += 1

    # -------------------------
    # GET CONTEXT
    # -------------------------
    def get_context(self):
        now = datetime.datetime.now()
        current_time = time.time()

        hour = now.hour

        # -------------------------
        # TIME PHASE
        # -------------------------
        if 5 <= hour < 12:
            phase = "morning"
        elif 12 <= hour < 17:
            phase = "afternoon"
        elif 17 <= hour < 21:
            phase = "evening"
        else:
            phase = "late_night"

        # -------------------------
        # IDLE DETECTION
        # -------------------------
        idle_seconds = int(current_time - self.last_user_input_time)

        if idle_seconds < 30:
            idle_state = "active"
        elif idle_seconds < 120:
            idle_state = "short_idle"
        else:
            idle_state = "idle"

        # -------------------------
        # SESSION LENGTH
        # -------------------------
        session_duration = int(current_time - self.session_start_time)

        # -------------------------
        # MOOD HINT
        # -------------------------
        if phase == "late_night":
            mood = "tired"
        elif phase == "morning":
            mood = "fresh"
        else:
            mood = "neutral"

        # -------------------------
        # CONVERSATION HOOKS
        # -------------------------
        hooks = self.generate_hooks(phase, idle_state, session_duration)

        return {
            "time": now.strftime("%H:%M"),
            "day": now.strftime("%A"),
            "phase": phase,
            "idle_state": idle_state,
            "idle_seconds": idle_seconds,
            "session_duration": session_duration,
            "interaction_count": self.interaction_count,
            "mood": mood,
            "hooks": hooks
        }

    # -------------------------
    # HOOK GENERATOR
    # -------------------------
    def generate_hooks(self, phase, idle_state, session_duration):

        hooks = []

        # Time-based
        if phase == "late_night":
            hooks.append("it's getting late")
        elif phase == "morning":
            hooks.append("day just started")
        elif phase == "evening":
            hooks.append("winding down time")

        # Idle-based
        if idle_state == "idle":
            hooks.append("user has been quiet for a while")

        # Long session
        if session_duration > 1800:
            hooks.append("user has been active for long time")

        return hooks