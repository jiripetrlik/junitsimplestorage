from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Numeric, String, DateTime, ForeignKey, and_, or_, func
from sqlalchemy.orm import sessionmaker, relationship, lazyload
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class JunitDatabase:
    def __init__(self, engine, scopedSession):
        self.engine = engine
        self.scopedSession = scopedSession
    
    def createSchema(self):
        Base.metadata.create_all(self.engine)

    def numberOfTestRuns(self):
        result = self.scopedSession.query(func.count(JunitTestRun.id)).one()
        return result[0]

    def getTestRuns(self, page, items):
        result = self.scopedSession.query(JunitTestRun).order_by(JunitTestRun.id).offset((page - 1) * items).limit(items).all()
        return result

    def insertTestRuns(self, testRuns, labels = {}):
        importTime = datetime.now()

        for testRun in testRuns:
            testRun.importTime = importTime

            testRun.labels = []
            for key in labels:
                label = Label()
                label.testRun = testRun
                label.key = key
                label.value = labels[key]

                testRun.labels.append(label)
        self.scopedSession.add_all(testRuns)

        self.scopedSession.commit()

        testRunIds = []
        for testRun in testRuns:
            testRunIds.append(testRun.id)
        
        return testRunIds

    def queryTestRuns(self, q):
        if ("labels" in q) and (len(q["labels"]) > 0):
            return self.__queryTestRunsWithLabels(q)
        else:
            return self.__queryTestRunsWithoutLabels(q)

    def __queryTestRunsWithoutLabels(self, q):
        query = self.scopedSession.query(JunitTestRun)
        
        query = self.__basicQueryFilter(q, query)
        query.order_by(JunitTestRun.id)

        return query.all()

    def __queryTestRunsWithLabels(self, q):
        query = self.scopedSession.query(JunitTestRun.id)
        conditions = []
        for label in q["labels"]:
            conditions.append(and_(Label.key == label, Label.value == q["labels"][label]))
        query = query.filter(or_(*conditions))
        query = query.join(Label, JunitTestRun.id == Label.testRun)
        query = query.group_by(JunitTestRun.id)
        query = query.having(func.count(JunitTestRun.id) == len(q["labels"]))
        
        query = self.__basicQueryFilter(q, query)
        query.order_by(JunitTestRun.id)
        testRunIds = query.all()
        testRunIds = list(map(lambda x : x[0], testRunIds))

        query = self.scopedSession.query(JunitTestRun)
        query = query.filter(JunitTestRun.id.in_(testRunIds))

        return query.all()

    def __basicQueryFilter(self, q, query):
        query = self.__filterListInQuery(q, "id", JunitTestRun.id, query)
        if ("minImportTime" in q) and (len(q["minImportTime"]) > 0):
            t = datetime.fromisoformat(q["minImportTime"])
            query = query.filter(JunitTestRun.importTime > t)
        if ("maxImportTime" in q) and (len(q["maxImportTime"]) > 0):
            t = datetime.fromisoformat(q["maxImportTime"])
            query = query.filter(JunitTestRun.importTime < t)
        query = self.__filterListInQuery(q, "testSuiteName", JunitTestRun.testSuiteName, query)
        if ("minTimeDate" in q) and (len(q["minTimeDate"]) > 0):
            t = datetime.fromisoformat(q["minTimeDate"])
            query = query.filter(JunitTestRun.timestamp > t)
        if ("maxTimeDate" in q) and (len(q["maxTimeDate"]) > 0):
            t = datetime.fromisoformat(q["maxTimeDate"])
            query = query.filter(JunitTestRun.timestamp < t)
        query = self.__filterListInQuery(q, "hostname", JunitTestRun.hostname, query)
        query = self.__filterListInQuery(q, "name", JunitTestRun.name, query)
        query = self.__filterListInQuery(q, "classname", JunitTestRun.classname, query)
        if "timeIsLower" in q:
            query = query.filter(JunitTestRun.time < q["timeIsLower"])
        if "timeIsHigher" in q:
            query = query.filter(JunitTestRun.time > q["timeIsHigher"])
        query = self.__filterListInQuery(q, "state", JunitTestRun.state, query)

        return query

    def __filterListInQuery(self, queryDict, queryParameter, tableColumn, databaseQuery):
        if (queryParameter in queryDict) and (len(queryDict[queryParameter]) > 0):
            databaseQuery = databaseQuery.filter(tableColumn.in_(queryDict[queryParameter]))

        return databaseQuery

    def deleteTestRun(self, id):
        testRun = self.scopedSession.query(JunitTestRun).filter(JunitTestRun.id == id).one()
        self.scopedSession.delete(testRun)
        self.scopedSession.commit()

    def getEngine(self):
        return self.engine

class JunitTestRun(Base):
    __tablename__ = "test_run"

    id = Column(Integer, primary_key=True)
    importTime = Column(DateTime)
    testSuiteName = Column(String(255))
    timestamp = Column(DateTime)
    hostname = Column(String(255))
    name = Column(String(255))
    classname = Column(String(255))
    time = Column(Numeric)
    state = Column(String(255))
    message = Column(String(255))
    labels = relationship("Label", back_populates = "testRuns", lazy = "joined", cascade = "all, delete, delete-orphan")

    def as_dict(self):
        dictionary = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        labels = {}
        for label in self.labels:
            labels[label.key] = label.value
        dictionary["labels"] = labels
        return dictionary

class Label(Base):
    __tablename__ = "label"

    id = Column(Integer, primary_key=True)
    testRun = Column(Integer, ForeignKey('test_run.id'), nullable=False)
    key = Column(String(255), nullable=False)
    value = Column(String(255), nullable=False)

    testRuns = relationship("JunitTestRun", back_populates = "labels")