import pytest
import os.path

EXAMPLE_JUNIT_FILE = "tests/junit-report-example.xml"

@pytest.fixture
def connectionString(tmpdir):
    sqlLiteFile = tmpdir.join("test_database.db")
    sqlLiteFilePath = os.path.abspath(sqlLiteFile)
    connectionString = "sqlite:///" + sqlLiteFilePath

    return connectionString

@pytest.fixture
def exampleJunitString():
    junitFile = open(EXAMPLE_JUNIT_FILE)
    junitString = junitFile.read()
    junitFile.close()

    return junitString
