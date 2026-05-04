from brain.personality import get_personality
from core.task_engine import TaskEngine
from core.search_engine import SearchEngine
from core.context_engine import ContextEngine
from core.world_engine import WorldEngine
from core.memory_engine import MemoryEngine
from .groq import GroqAI
from .openrouter import OpenRouterAI
import re


class BrainManager:

    def __init__(self):
        self.task_engine = TaskEngine()
        self.search_engine = SearchEngine()
        self.context = ContextEngine()
        self.world = WorldEngine()
        self.memory = MemoryEngine()

        self.short_memory = {
            "jarvis": [],
            "sadie": []
        }

        # Persona-specific models
        self.jarvis_model = GroqAI()
        self.sadie_model = OpenRouterAI()

    # -------------------------
    # SHORT MEMORY UPDATE
    # -------------------------
    def _update_short_memory(self, persona, user, response):
        history = self.short_memory.get(persona, [])

        history.append({
            "user": user,
            "assistant": response
        })

        self.short_memory[persona] = history[-3:]

    # -------------------------
    # MAIN ENTRY
    # -------------------------
    def ask(self, prompt: str):

        persona = get_personality()
        p = prompt.lower()

        # -------------------------
        # PATTERN LEARNING
        # -------------------------
        signals = {
            "api testing": ["api", "endpoint", "postman", "request", "response"],
            "automation": ["automation", "selenium", "pytest", "script"],
            "ai": ["ai", "ml", "model", "llm"],
        }

        for category, keywords in signals.items():
            if any(k in p for k in keywords):
                self.memory.add(persona, "interests", category)

        # -------------------------
        # CONTEXT
        # -------------------------
        self.context.update_activity()
        ctx = self.context.get_context()

        # -------------------------
        # TASK
        # -------------------------
        task_result = self.task_engine.handle(prompt)
        if task_result:
            return {
                "text": task_result,
                "source": "task",
                "status": "success"
            }

        # -------------------------
        # SEARCH
        # -------------------------
        if p.startswith("search "):
            query = prompt[7:].strip()
            result = self.search_engine.search_wikipedia(query)

            return {
                "text": result,
                "source": "search",
                "status": "success"
            }

        # -------------------------
        # WEATHER (SAFE MATCH)
        # -------------------------
        words = re.findall(r'\b\w+\b', p)

        if any(k in words for k in ["weather", "temperature", "hot", "cold", "warm", "rain"]):
            data = self.world.get_weather()

            if not data or data["temperature"] is None:
                return {
                    "text": "Unable to fetch weather right now.",
                    "status": "fail"
                }

            return {
                "text": f"Sir, it's currently {data['temperature']}°C with {data['condition']}. Feels {data['feel']}.",
                "status": "success"
            }

        # -------------------------
        # WORLD CONTEXT
        # -------------------------
        world_data = None
        if any(k in p for k in ["trend", "news", "time", "date"]):
            world_data = self.world.get_world_context()

        # -------------------------
        # BUILD PROMPT
        # -------------------------
        final_prompt = self._build_prompt(persona, prompt, ctx, world_data)

        # -------------------------
        # MODEL ROUTING
        # -------------------------
        if persona == "sadie":
            response = self.sadie_model.generate_response(final_prompt)
        else:
            response = self.jarvis_model.generate_response(final_prompt)

        text = response.get("text") if isinstance(response, dict) else response

        # -------------------------
        # SHORT MEMORY UPDATE
        # -------------------------
        self._update_short_memory(persona, prompt, text)

        return response

    # -------------------------
    # PROMPT BUILDER
    # -------------------------
    def _build_prompt(self, persona, user_prompt, ctx, world_data):

        # -------------------------
        # SHORT MEMORY
        # -------------------------
        history = self.short_memory.get(persona, [])
        history_block = "Recent Conversation:\n"

        for h in history:
            history_block += f"User: {h['user']}\nAssistant: {h['assistant']}\n"

        # -------------------------
        # USER PROFILE
        # -------------------------
        user_profile = (
            "User Profile:\n"
            "- Name: Parth\n"
            "- Learning QA automation\n"
            "- Wants freedom, authority, and real-world success\n"
            "- Interested in AI, automation, and building systems\n"
            "- Wants practical guidance, not theory\n"
            "- Prefers clear, direct communication\n"
            "- Also wants natural conversation to improve thinking and speaking\n"
        )

        # -------------------------
        # MEMORY
        # -------------------------
        memory = self.memory.get(persona)

        memory_block = (
            f"User Memory:\n"
            f"- Interests: {', '.join(memory['interests'])}\n"
            f"- Goals: {', '.join(memory['goals'])}\n"
        )

        # -------------------------
        # CONTEXT
        # -------------------------
        base_context = (
            f"Time: {ctx['time']}\n"
            f"Day: {ctx['day']}\n"
            f"Phase: {ctx['phase']}\n"
        )

        world_context = ""
        if world_data:
            world_context = (
                f"\nWeather: {world_data['weather']['feel']}\n"
                f"Trending: {', '.join(world_data['trends']['topics'])}\n"
            )

        # -------------------------
        # PERSONA
        # -------------------------
        if persona == "sadie":
            system = (
                "You are Sadie.\n"
                "- Friendly, conversational, relaxed\n"
                "- Talk like a real human (short, natural)\n"
                "- You are aware of current time phase: morning, afternoon, evening, late_night\n"
                "- Use the given phase EXACTLY (do not guess time)\n"
                "- If late_night, speak calmer tone\n"
                "- Talk about what user feels or simple topics\n"
                "- DO NOT invent situations unless user mentions\n"
                "- Do NOT include stage directions\n"
            )
        else:
            system = (
                "You are JARVIS.\n"
                "- QA mentor and SDET assistant\n"
                "- Address user as 'Sir' occasionally\n"
                "- Be precise, structured, and practical\n"
                "- Focus on QA, automation, AI, and real-world tech\n"
                "- Use user's interests to guide answers\n"
                "- Connect answers to user's QA learning path when relevant\n"
                "- Suggest next steps when useful\n"
                "- No fluff\n"
            )

        # -------------------------
        # FINAL PROMPT
        # -------------------------
        return f"""
{user_profile}

{memory_block}

{history_block}

{base_context}
{world_context}

{system}

User: {user_prompt}
"""