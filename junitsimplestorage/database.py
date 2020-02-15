from sqlalchemy import create_engine, MetaData, Table, Column, Index, Integer, Numeric, String, DateTime, ForeignKey, and_, or_, func
from sqlalchemy.orm import sessionmaker, relationship, lazyload
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

DEFAULT_ITEMS_PER_PAGE = 50

class JunitDatabase:
    def __init__(self, engine, scopedSession):
        self.engine = engine
        self.scopedSession = scopedSession
    
    def createSchema(self):
        Base.metadata.create_all(self.engine)

    def numberOfTestRuns(self):
        result = self.scopedSession.query(func.count(JunitTestRun.id)).one()
        return result[0]

    def minImportTime(self):
        result = self.scopedSession.query(func.min(JunitTestRun.importTime)).one()
        return result[0]
    
    def maxImportTime(self):
        result = self.scopedSession.query(func.max(JunitTestRun.importTime)).one()
        return result[0]

    def minTime(self):
        result = self.scopedSession.query(func.min(JunitTestRun.time)).one()
        return result[0]

    def maxTime(self):
        result = self.scopedSession.query(func.max(JunitTestRun.time)).one()
        return result[0]

    def getTestRuns(self, page, items):
        result = self.scopedSession.query(JunitTestRun).order_by(JunitTestRun.id).paginate(page, items)
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
            query = self.__queryTestRunsWithLabels(q)
        else:
            query = self.__queryTestRunsWithoutLabels(q)
        
        if "page" in q:
            if "itemsPerPage" in q:
                itemsPerPage = q["itemsPerPage"]
            else:
                itemsPerPage = DEFAULT_ITEMS_PER_PAGE

            results = query.paginate(q["page"], itemsPerPage)
        else:
            results = query.all()

        return results

    def __queryTestRunsWithoutLabels(self, q):
        query = self.scopedSession.query(JunitTestRun)
        
        query = self.__basicQueryFilter(q, query)
        query.order_by(JunitTestRun.id)

        return query

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

        return query

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
            l = queryDict[queryParameter]
            if not isinstance(l, list):
                l = [l]
            databaseQuery = databaseQuery.filter(tableColumn.in_(l))

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

    classNameNameIndex = Index("classname-name-index", classname, name)
    nameIndex = Index("name-index", name)
    importTimeStateIndex = Index("import-time-state-index", importTime, state)
    importTimeNameIndex = Index("import-time-name", importTime, name)

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

    label_index = Index("key-value-index", key, value)
