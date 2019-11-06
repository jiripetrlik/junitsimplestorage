from junit_simple_storage.database import JunitDatabase, JunitTestRun
from sqlalchemy import create_engine, inspect
import os.path

def test_create_schema(tmpdir):
    sqlLiteFile = tmpdir.join("test_database.db")
    sqlLiteFilePath = os.path.abspath(sqlLiteFile)
    connectionString = "sqlite:///" + sqlLiteFilePath
    database = JunitDatabase(connectionString)
    database.connect()
    database.createSchema()
    database.dispose()

    expectedTables = ["test_run"]
    engine = create_engine(connectionString)
    inspector = inspect(engine)
    for tableName in expectedTables:
        assert tableName in inspector.get_table_names()
    engine.dispose()
