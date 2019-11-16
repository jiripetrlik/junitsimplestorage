from junit_simple_storage.database import JunitDatabase, JunitTestRun
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
import datetime
from junit_simple_storage.junit import loadJunitTestRuns

def test_create_schema(connectionString):
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

def test_add_test_run(connectionString):
    database = JunitDatabase(connectionString)
    database.connect()
    database.createSchema()

    testRun = JunitTestRun()
    testRun.id = 5
    testRun.testSuiteName = "Test suite 1"
    testRun.timestamp = datetime.datetime.strptime("2019-01-01 12:04:05", '%Y-%m-%d %H:%M:%S')
    testRun.hostname = "host 1"
    testRun.name = "Test run 1"
    testRun.classname = "Class 1"
    testRun.file = "/file1.txt"
    testRun.state = "passed"
    database.insertTestRun(testRun)
    database.dispose()

    database.connect()
    engine = database.getEngine()
    Session = sessionmaker(bind = engine)
    session = Session()
    items = session.query(JunitTestRun).count()
    assert items == 1
    database.dispose()

def test_save_test_runs(connectionString):
    database = JunitDatabase(connectionString)
    database.connect()
    database.createSchema()

    testRuns = loadJunitTestRuns("tests/junit-report-example.xml")
    database.insertTestRuns(testRuns)

def test_save_test_runs_with_labels(connectionString):
    database = JunitDatabase(connectionString)
    database.connect()
    database.createSchema()

    labels = { "key1" : "value1", "key2" : "value2" }
    testRuns = loadJunitTestRuns("tests/junit-report-example.xml")
    database.insertTestRuns(testRuns, labels)
