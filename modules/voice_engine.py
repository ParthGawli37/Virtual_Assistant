import asyncio
import edge_tts
import tempfile
import os
import threading
import pygame
import time


class VoiceEngine:
    def __init__(self):
        self.enabled = False

        pygame.mixer.init()


        # 🔥 Best female neural voice (calm tone)
        self.voice = "en-US-AriaNeural"   # to change voice change the value in "" to available models.

    def speak(self, text):
        if not self.enabled:
            return

        def run():
            try:
                asyncio.run(self._generate_and_play(text))
            except Exception as e:
                print("Voice Error:", e)

        threading.Thread(target=run).start()

    async def _generate_and_play(self, text):
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        temp_path = temp_file.name
        temp_file.close()

        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(temp_path)

        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.music.unload()
        os.remove(temp_path)