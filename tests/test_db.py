# src/p5/test_database.py

from sqlalchemy import text

from p5.database import engine


def test_connection():
    """Vérifie que PostgreSQL répond."""

    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1