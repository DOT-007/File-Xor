import asyncio
import sqlite3
import asyncpg
from config import BotInfoConfig


# ------------------------------
# Database setup (async)
# ------------------------------
class BanDB:
    def __init__(self, db_url=None):
        self.db_url = db_url
        self.sqlite_conn = None
        self.pg_pool = None

    async def init(self):
        if self.db_url:
            # PostgreSQL
            self.pg_pool = await asyncpg.create_pool(self.db_url)
            async with self.pg_pool.acquire() as conn:
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS bans (
                        user_id BIGINT PRIMARY KEY,
                        reason TEXT,
                        banned_at TIMESTAMP DEFAULT NOW()
                    )
                """)
        else:
            # SQLite fallback
            self.sqlite_conn = sqlite3.connect("bans.db", check_same_thread=False)
            cur = self.sqlite_conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS bans (
                    user_id INTEGER PRIMARY KEY,
                    reason TEXT,
                    banned_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.sqlite_conn.commit()

    async def add_ban(self, user_id: int, reason: str = None):
        if self.pg_pool:
            async with self.pg_pool.acquire() as conn:
                await conn.execute(
                    "INSERT INTO bans (user_id, reason) VALUES ($1, $2) ON CONFLICT (user_id) DO NOTHING",
                    user_id, reason
                )
        else:
            cur = self.sqlite_conn.cursor()
            cur.execute("INSERT OR IGNORE INTO bans (user_id, reason) VALUES (?, ?)", (user_id, reason))
            self.sqlite_conn.commit()

    async def remove_ban(self, user_id: int):
        if self.pg_pool:
            async with self.pg_pool.acquire() as conn:
                await conn.execute("DELETE FROM bans WHERE user_id = $1", user_id)
        else:
            cur = self.sqlite_conn.cursor()
            cur.execute("DELETE FROM bans WHERE user_id = ?", (user_id,))
            self.sqlite_conn.commit()

    async def get_bans(self):
        if self.pg_pool:
            async with self.pg_pool.acquire() as conn:
                rows = await conn.fetch("SELECT user_id, reason, banned_at FROM bans")
                return [(r["user_id"], r["reason"], str(r["banned_at"])) for r in rows]
        else:
            cur = self.sqlite_conn.cursor()
            cur.execute("SELECT user_id, reason, banned_at FROM bans")
            return cur.fetchall()

# ------------------------------
# Initialize DB
# ------------------------------
# Create the DB instance using the configured DATABASE_URL (if present)
db = BanDB(getattr(BotInfoConfig, 'DATABASE_URL', None) if getattr(BotInfoConfig, 'DATABASE_URL', None) else None)


# Initialize the DB in a safe manner.
# - If an asyncio event loop is already running, schedule the init coroutine
#   as a background task and store it on the DB instance as `init_task` so
#   callers can await it via `ensure_db_ready()`.
# - If no loop is running, run the initializer synchronously using
#   `asyncio.run()` (creates its own loop) so scripts that import this module
#   still get a ready DB.

async def _init_db():
    await db.init()

# Default: no init task yet
db.init_task = None

try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = None

if loop and loop.is_running():
    # running loop present (e.g. Pyrogram). Schedule initialization and keep
    # the task so other modules can await completion.
    db.init_task = loop.create_task(_init_db())
else:
    # No running loop: run the initializer synchronously (blocks here while
    # creating and closing a temporary event loop). This mirrors prior
    # behavior but avoids calling run_until_complete on a possibly-running loop.
    try:
        asyncio.run(_init_db())
    except Exception:
        # Allow import to succeed even if DB init fails; application code
        # can call/await db.init() later or inspect db.init_task.
        db.init_task = None


async def ensure_db_ready(timeout: float | None = None):
    """Await DB initialization if it was scheduled on the running loop.

    Callers (like plugins) should await this before using `db` to ensure
    initialization completed. If initialization already ran synchronously,
    this returns immediately.
    """
    task = getattr(db, 'init_task', None)
    if task is None:
        return
    if timeout is None:
        await task
    else:
        await asyncio.wait_for(task, timeout=timeout)




