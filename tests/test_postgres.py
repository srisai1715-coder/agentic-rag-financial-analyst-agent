from app.database.postgres import CREATE_TABLE_SQL


def test_postgres_schema_contains_agent_runs():
    assert "CREATE TABLE IF NOT EXISTS agent_runs" in CREATE_TABLE_SQL
    assert "query TEXT NOT NULL" in CREATE_TABLE_SQL
    assert "answer TEXT" in CREATE_TABLE_SQL
    assert "verification_status TEXT" in CREATE_TABLE_SQL
