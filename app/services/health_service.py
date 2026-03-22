from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def check_database_health(db: AsyncSession) -> bool:
    """Return True when the database connection is alive."""
    try:
        await db.execute(select(1))
        return True
    except Exception:
        return False
