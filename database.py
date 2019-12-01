from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Numeric, String, DateTime, ForeignKey, or_
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class JunitDatabase:
    def __init__(self, engine, scopedSession):
        self.engine = engine
        self.scopedSession = scopedSession
    
    def createSchema(self):
        Base.metadata.create_all(self.engine)

    def getTestRuns(self, page, items):
        result = self.scopedSession.query(JunitTestRun).order_by(JunitTestRun.id).offset((page - 1) * items).limit(items).all()
        return result

    def insertTestRuns(self, testRuns, labels = {}):
        for testRun in testRuns:
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
        query = self.scopedSession.query(JunitTestRun)
        if ("id" in q) and (len(q["id"]) > 0):
            conditions = []
            for id in q["id"]:
                conditions.append(JunitTestRun.id == id)
            query = query.filter(or_(*conditions))
        if ("testSuiteName" in q) and (len(q["testSuiteName"]) > 0):
            conditions = []
            for testSuiteName in q["testSuiteName"]:
                conditions.append(JunitTestRun.testSuiteName == testSuiteName)
            query = query.filter(or_(*conditions))
        if ("minTimeDate" in q) and (len(q["minTimeDate"]) > 0):
            t = datetime.fromisoformat(q["minTimeDate"])
            query = query.filter(JunitTestRun.timestamp > t)
        if ("maxTimeDate" in q) and (len(q["maxTimeDate"]) > 0):
            t = datetime.fromisoformat(q["maxTimeDate"])
            query = query.filter(JunitTestRun.timestamp < t)
        if ("hostname" in q) and (len(q["hostname"]) > 0):
            conditions = []
            for hostname in q["hostname"]:
                conditions.append(JunitTestRun.hostname == hostname)
            query = query.filter(or_(*conditions))
        if ("name" in q) and (len(q["name"]) > 0):
            conditions = []
            for name in q["name"]:
                conditions.append(JunitTestRun.name == name)
            query = query.filter(or_(*conditions))
        if ("classname" in q) and (len(q["classname"]) > 0):
            conditions = []
            for classname in q["classname"]:
                conditions.append(JunitTestRun.classname == classname)
            query = query.filter(or_(*conditions))
        if "timeIsLower" in q:
            query = query.filter(JunitTestRun.time < q["timeIsLower"])
        if "timeIsHigher" in q:
            query = query.filter(JunitTestRun.time > q["timeIsHigher"])
        if ("state" in q) and (len(q["state"]) > 0):
            conditions = []
            for state in q["state"]:
                conditions.append(JunitTestRun.state == state)
            query = query.filter(or_(*conditions))
        query.order_by(JunitTestRun.id)

        return query.all()

    def getEngine(self):
        return self.engine

class JunitTestRun(Base):
    __tablename__ = "test_run"

    id = Column(Integer, primary_key=True)
    testSuiteName = Column(String)
    timestamp = Column(DateTime)
    hostname = Column(String)
    name = Column(String)
    classname = Column(String)
    time = Column(Numeric)
    state = Column(String)
    message = Column(String)
    labels = relationship("Label", back_populates = "testRuns", lazy = "joined")

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
    key = Column(String, nullable=False)
    value = Column(String, nullable=False)

    testRuns = relationship("JunitTestRun", back_populates = "labels")