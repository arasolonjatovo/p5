# src/p5/test_database.py

from sqlalchemy import text

from p5.database import engine


def test_connection():
    """Vérifie que PostgreSQL répond."""

    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1


def test_buildings_table_exists():
    """Vérifie que la table buildings existe."""

    with engine.connect() as conn:
        result = conn.execute(
            text(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.tables
                    WHERE table_name = 'buildings'
                )
                """
            )
        )

        assert result.scalar() is True


def test_buildings_not_empty():
    """Vérifie que le CSV a bien été importé."""

    with engine.connect() as conn:
        result = conn.execute(
            text(
                """
                SELECT COUNT(*)
                FROM buildings
                """
            )
        )

        assert result.scalar_one() > 0


def test_ml_tables_exist():
    """Vérifie les tables de traçabilité."""

    tables = ["ml_requests", "ml_predictions"]

    with engine.connect() as conn:
        for table in tables:
            result = conn.execute(
                text(
                    f"""
                    SELECT EXISTS (
                        SELECT 1
                        FROM information_schema.tables
                        WHERE table_name = '{table}'
                    )
                    """
                )
            )

            assert result.scalar() is True
