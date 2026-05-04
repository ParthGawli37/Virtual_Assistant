from core.memory_engine import MemoryEngine

m = MemoryEngine()

m.add("interests", "api testing")
m.add("interests", "api testing")

print(m.get())