import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "demo.db"


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS memos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL
            )
            """
        )


def add_memo(title: str, content: str = "") -> int:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with connect() as conn:
        cur = conn.execute(
            "INSERT INTO memos(title, content, created_at) VALUES (?, ?, ?)",
            (title, content, ts),
        )
        return int(cur.lastrowid)


def list_memos() -> list[sqlite3.Row]:
    with connect() as conn:
        return list(
            conn.execute("SELECT id, title, content, created_at FROM memos ORDER BY id DESC")
        )


if __name__ == "__main__":
    init_db()
    new_id = add_memo("스프린트 회의", "API 일정과 UI 마감을 논의함")
    print(f"저장된 메모 id={new_id}")
    print("--- 목록 ---")
    for row in list_memos():
        print(f"[{row['id']}] {row['title']} ({row['created_at']})")
        print(f"    {row['content']}")
    print(f"\nDB 파일 위치: {DB_PATH}")