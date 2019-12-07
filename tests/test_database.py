from database import JunitDatabase, JunitTestRun, Label
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, scoped_session
import datetime
from junit import loadJunitTestRuns

def test_create_schema(connectionString):
    engine = create_engine(connectionString)
    engine.connect()
    session = __scopedSession(engine)
    database = JunitDatabase(engine, session)
    database.createSchema()
    engine.dispose()

    expectedTables = ["test_run"]
    engine = create_engine(connectionString)
    inspector = inspect(engine)
    for tableName in expectedTables:
        assert tableName in inspector.get_table_names()
    engine.dispose()

def test_save_test_runs(connectionString, exampleJunitString):
    engine = create_engine(connectionString)
    engine.connect()
    session = __scopedSession(engine)
    database = JunitDatabase(engine, session)
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

def test_number_of_test_runs(connectionString, exampleJunitString):
    engine = create_engine(connectionString)
    engine.connect()
    session = __scopedSession(engine)
    database = JunitDatabase(engine, session)
    database.createSchema()

    testRuns = loadJunitTestRuns(exampleJunitString)
    numberOfTestRuns = len(testRuns)
    database.insertTestRuns(testRuns)

    assert database.numberOfTestRuns() == numberOfTestRuns

def test_min_import_time(connectionString, exampleJunitString):
    engine = create_engine(connectionString)
    engine.connect()
    session = __scopedSession(engine)
    database = JunitDatabase(engine, session)
    database.createSchema()

    testRuns = loadJunitTestRuns(exampleJunitString)
    database.insertTestRuns(testRuns)

    minImportTime = database.minImportTime()
    assert minImportTime != None

def test_max_import_time(connectionString, exampleJunitString):
    engine = create_engine(connectionString)
    engine.connect()
    session = __scopedSession(engine)
    database = JunitDatabase(engine, session)
    database.createSchema()

    testRuns = loadJunitTestRuns(exampleJunitString)
    database.insertTestRuns(testRuns)

    maxImportTime = database.maxImportTime()
    assert maxImportTime != None

def test_min_time(connectionString, exampleJunitString):
    engine = create_engine(connectionString)
    engine.connect()
    session = __scopedSession(engine)
    database = JunitDatabase(engine, session)
    database.createSchema()

    testRuns = loadJunitTestRuns(exampleJunitString)
    database.insertTestRuns(testRuns)

    minTime = database.minTime()
    assert minTime != None

def test_max_time(connectionString, exampleJunitString):
    engine = create_engine(connectionString)
    engine.connect()
    session = __scopedSession(engine)
    database = JunitDatabase(engine, session)
    database.createSchema()

    testRuns = loadJunitTestRuns(exampleJunitString)
    database.insertTestRuns(testRuns)

    maxTime = database.maxTime()
    assert maxTime != None

def test_save_test_runs_with_labels(connectionString, exampleJunitString):
    engine = create_engine(connectionString)
    engine.connect()
    session = __scopedSession(engine)
    database = JunitDatabase(engine, session)
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

def test_query_by_name(connectionString, exampleJunitString):
    engine = create_engine(connectionString)
    engine.connect()
    session = __scopedSession(engine)
    database = JunitDatabase(engine, session)
    database.createSchema()

    testRuns = loadJunitTestRuns(exampleJunitString)
    database.insertTestRuns(testRuns)

    testRuns = database.queryTestRuns({"name" : ["test_something1", "test_something3"]})
    assert len(testRuns) == 2

    engine.dispose()

def test_query_by_timestamp(connectionString, exampleJunitString):
    engine = create_engine(connectionString)
    engine.connect()
    session = __scopedSession(engine)
    database = JunitDatabase(engine, session)
    database.createSchema()

    testRuns = loadJunitTestRuns(exampleJunitString)
    database.insertTestRuns(testRuns)

    minTimeDate = datetime.datetime.now() - datetime.timedelta.days(1)
    maxTimeDate = datetime.datetime.now() + datetime.timedelta.days(1)
    testRuns = database.queryTestRuns({
        "minImportTime" : minTimeDate,
        "maxImportTime" : maxTimeDate
        })
    assert len(testRuns) > 0

def test_query_by_timestamp(connectionString, exampleJunitString):
    engine = create_engine(connectionString)
    engine.connect()
    session = __scopedSession(engine)
    database = JunitDatabase(engine, session)
    database.createSchema()

    testRuns = loadJunitTestRuns(exampleJunitString)
    database.insertTestRuns(testRuns)

    testRuns = database.queryTestRuns({
        "timeIsLower" : 2.5,
        "timeIsHigher" : 1.0
        })
    assert len(testRuns) == 1
    assert testRuns[0].name == "test_something2"

def test_query_by_timestamp(connectionString, exampleJunitString):
    engine = create_engine(connectionString)
    engine.connect()
    session = __scopedSession(engine)
    database = JunitDatabase(engine, session)
    database.createSchema()

    testRuns = loadJunitTestRuns(exampleJunitString)
    database.insertTestRuns(testRuns)
    
    testRuns = database.queryTestRuns({
        "minTimeDate" : "2019-11-01 10:00:00",
        "maxTimeDate" : "2019-11-30 20:15:05"
        })
    assert len(testRuns) == 4

def test_query_by_labels(connectionString, exampleJunitString):
    engine = create_engine(connectionString, echo=True)
    engine.connect()
    session = __scopedSession(engine)
    database = JunitDatabase(engine, session)
    database.createSchema()

    testRuns = loadJunitTestRuns(exampleJunitString)
    numberOfTestRuns = len(testRuns)
    database.insertTestRuns(testRuns)
    testRuns = loadJunitTestRuns(exampleJunitString)
    database.insertTestRuns(testRuns, {"label1" : "value1"})
    testRuns = loadJunitTestRuns(exampleJunitString)
    database.insertTestRuns(testRuns, {"label1" : "value1", "label2" : "value2"})

    testRuns = database.queryTestRuns({
            "labels" : {
                "label1" : "value1",
            }
        })
    assert len(testRuns) == 2 * numberOfTestRuns
    
    testRuns = database.queryTestRuns({
            "labels" : {
                "label1" : "value1",
                "label2" : "value2",
            }
        })
    assert len(testRuns) == numberOfTestRuns

def test_delete_test_run(connectionString, exampleJunitString):
    engine = create_engine(connectionString)
    engine.connect()
    session = __scopedSession(engine)
    database = JunitDatabase(engine, session)
    database.createSchema()

    testRuns = loadJunitTestRuns(exampleJunitString)
    database.insertTestRuns(testRuns, {"label1" : "value1"})

    testRuns = database.getTestRuns(1, 100)
    testRunIds = []
    for testRun in testRuns:
        testRunIds.append(testRun.id)
    assert 2 in testRunIds
    assert session.query(Label).filter(Label.testRun == 2).count() > 0

    database.deleteTestRun(2)

    testRuns = database.getTestRuns(1, 100)
    testRunIds = []
    for testRun in testRuns:
        testRunIds.append(testRun.id)
    assert 2 not in testRunIds
    assert session.query(Label).filter(Label.testRun == 2).count() == 0

def __scopedSession(engine):
    sessionFactory = sessionmaker(bind=engine)
    scopedSession = scoped_session(sessionFactory)

    return scopedSession
