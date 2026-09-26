import json
import sqlite3
from datetime import UTC, datetime


class AuditLog:
    def __init__(self, path: str = "hitl_audit.db"):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_events (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              thread_id TEXT NOT NULL,
              event_type TEXT NOT NULL,
              payload TEXT NOT NULL,
              created_at TEXT NOT NULL
            )
            """
        )
        self.conn.commit()

    def write(self, thread_id: str, event_type: str, payload: dict):
        with self.conn:
            self.conn.execute(
                "INSERT INTO audit_events(thread_id,event_type,payload,created_at) VALUES(?,?,?,?)",
                (
                    thread_id,
                    event_type,
                    json.dumps(payload, default=str),
                    datetime.now(UTC).isoformat(),
                ),
            )

    def read(self, thread_id: str) -> list[dict]:
        rows = self.conn.execute(
            "SELECT event_type,payload,created_at FROM audit_events WHERE thread_id=? ORDER BY id",
            (thread_id,),
        ).fetchall()
        return [
            {
                "event_type": row[0],
                "payload": json.loads(row[1]),
                "created_at": row[2],
            }
            for row in rows
        ]
