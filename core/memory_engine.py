import sqlite3


class MemoryEngine:

    def __init__(self, db_path="core/memory.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    # -------------------------
    # TABLE SETUP
    # -------------------------
    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                persona TEXT,
                category TEXT,
                value TEXT,
                count INTEGER DEFAULT 1,
                UNIQUE(persona, category, value)
            )
        """)
        self.conn.commit()

    # -------------------------
    # ADD / UPDATE MEMORY
    # -------------------------
    def add(self, persona, category, value):

        cursor = self.conn.execute(
            "SELECT count FROM memory WHERE persona=? AND category=? AND value=?",
            (persona, category, value)
        )

        row = cursor.fetchone()

        if row:
            self.conn.execute(
                "UPDATE memory SET count = count + 1 WHERE persona=? AND category=? AND value=?",
                (persona, category, value)
            )
        else:
            self.conn.execute(
                "INSERT INTO memory (persona, category, value, count) VALUES (?, ?, ?, 1)",
                (persona, category, value)
            )

        self.conn.commit()

    # -------------------------
    # GET MEMORY PER PERSONA
    # -------------------------
    def get(self, persona):

        cursor = self.conn.execute(
            "SELECT category, value, count FROM memory WHERE persona=? AND count >= 2",
            (persona,)
        )

        memory = {
            "preferences": [],
            "interests": [],
            "goals": []
        }

        for category, value, _ in cursor.fetchall():
            if category in memory:
                memory[category].append(value)

        return memory