"""Edge node simulation for aircraft telemetry."""

import json
import sqlite3
import time


class EdgeNode:
    def __init__(self, aircraft_id: str, db_path: str = "edge_outbox.db"):
        self.aircraft_id = aircraft_id
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS outbox
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             aircraft_id TEXT,
                             timestamp REAL,
                             payload TEXT,
                             synced INTEGER DEFAULT 0)""")

    def process_telemetry(self, raw_telemetry: list, rul_pred: float, health_score: float):
        """Process raw telemetry locally on the edge node and save to outbox if critical/warning."""
        # Instead of sending heavy raw_telemetry (e.g. 10MB/hr), we only send a 1KB JSON summary
        summary = {
            "rul": rul_pred,
            "health_score": health_score,
            "anomaly_detected": health_score < 75.0,
        }

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO outbox (aircraft_id, timestamp, payload) VALUES (?, ?, ?)",
                (self.aircraft_id, time.time(), json.dumps(summary)),
            )

    def sync_to_base(self, link_active: bool) -> int:
        """Attempt to flush outbox if link is active. Returns number of synced messages."""
        if not link_active:
            return 0

        synced_count = 0
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, payload FROM outbox WHERE synced = 0")
            rows = cursor.fetchall()

            for row in rows:
                msg_id, _payload = row
                # Simulate network send
                time.sleep(0.01)

                # Mark as synced
                cursor.execute("UPDATE outbox SET synced = 1 WHERE id = ?", (msg_id,))
                synced_count += 1

            conn.commit()

        return synced_count
