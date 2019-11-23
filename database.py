from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Numeric, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class JunitDatabase:
    def __init__(self, engine):
        self.engine = engine
    
    def createSchema(self):
        Base.metadata.create_all(self.engine)

    def getTestRuns(self, page, items):
        Session = sessionmaker(bind = self.engine)
        session = Session()

        result = session.query(JunitTestRun).order_by("id").offset((page - 1) * items).limit(items).all()
        return result

    def insertTestRun(self, testRun, labels = {}):
        Session = sessionmaker(bind = self.engine)
        session = Session()
        session.add(testRun)
        session.flush()

        for key in labels:
            label = Label(
                testRun = testRun.id,
                key = key,
                value = labels[key])

        session.commit()

    def insertTestRuns(self, testRuns, labels = {}):
        Session = sessionmaker(bind = self.engine)
        session = Session()

        session.add_all(testRuns)
        session.flush()

        testRunIds = []
        for testRun in testRuns:
            testRunIds.append(testRun.id)
            for key in labels:
                label = Label(
                    testRun = testRun.id,
                    key = key,
                    value = labels[key])
                session.add(label)

        session.commit()
        
        return testRunIds

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

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Label(Base):
    __tablename__ = "label"

    id = Column(Integer, primary_key=True)
    testRun = Column(Integer, ForeignKey('test_run.id'), nullable=False)
    key = Column(String, nullable=False)
    value = Column(String, nullable=False)
