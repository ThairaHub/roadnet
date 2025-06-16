import asyncio
import asyncpg
import os
import sys

async def wait_for_db():
    """Run migration only after the DB is up"""
    
    db_url = os.environ.get('DATABASE_URL')
    max_attempts = 20

    for attempt in range(1, max_attempts + 1):
        try:
            conn = await asyncpg.connect(dsn=db_url.replace("postgresql+asyncpg", "postgresql"))
            await conn.close()
            print("Database is ready!")
            return
        except Exception as e:
            print(f"Attempt {attempt}: Database not ready yet ({e})")
            await asyncio.sleep(1)

    print("Failed to connect to the database after multiple attempts.")
    sys.exit(1)

if __name__ == "__main__":
    asyncio.run(wait_for_db())
