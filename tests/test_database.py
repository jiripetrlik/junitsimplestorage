from database import JunitDatabase, JunitTestRun, Label
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
import datetime
from junit import loadJunitTestRuns

def test_create_schema(connectionString):
    engine = create_engine(connectionString)
    engine.connect()
    database = JunitDatabase(engine)
    database.createSchema()
    engine.dispose()

    expectedTables = ["test_run"]
    engine = create_engine(connectionString)
    inspector = inspect(engine)
    for tableName in expectedTables:
        assert tableName in inspector.get_table_names()
    engine.dispose()

def test_add_test_run(connectionString):
    engine = create_engine(connectionString)
    engine.connect()
    database = JunitDatabase(engine)
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
    engine.dispose()

    engine = create_engine(connectionString)
    engine.connect()
    engine = database.getEngine()
    Session = sessionmaker(bind = engine)
    session = Session()
    numberOfTestRuns = session.query(JunitTestRun).count()
    assert numberOfTestRuns == 1
    engine.dispose()

def test_save_test_runs(connectionString, exampleJunitString):
    engine = create_engine(connectionString)
    engine.connect()
    database = JunitDatabase(engine)
    database.createSchema()

    testRuns = loadJunitTestRuns(exampleJunitString)
    database.insertTestRuns(testRuns)
    engine.dispose()

    engine = create_engine(connectionString)
    Session = sessionmaker(bind = engine)
    session = Session()
    numberOfTestRuns = session.query(JunitTestRun).count()
    assert numberOfTestRuns > 0
    engine.dispose()

def test_save_test_runs_with_labels(connectionString, exampleJunitString):
    engine = create_engine(connectionString)
    engine.connect()
    database = JunitDatabase(engine)
    database.createSchema()

    labels = { "key1" : "value1", "key2" : "value2" }
    testRuns = loadJunitTestRuns(exampleJunitString)
    database.insertTestRuns(testRuns, labels)
    engine.dispose()

    engine = create_engine(connectionString)
    engine.connect()
    engine = database.getEngine()
    Session = sessionmaker(bind = engine)
    session = Session()
    numberOfTestRuns = session.query(JunitTestRun).count()
    assert numberOfTestRuns > 0
    numberOfLabels = session.query(Label).count()
    assert numberOfLabels > 0
    engine.dispose()
