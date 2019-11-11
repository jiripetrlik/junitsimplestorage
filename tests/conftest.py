import pytest
import os.path

@pytest.fixture
def connectionString(tmpdir):
    sqlLiteFile = tmpdir.join("test_database.db")
    sqlLiteFilePath = os.path.abspath(sqlLiteFile)
    connectionString = "sqlite:///" + sqlLiteFilePath

    return connectionString
