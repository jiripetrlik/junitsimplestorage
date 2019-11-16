from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Numeric, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class JunitDatabase:
    def __init__(self, connectionString):
        self.engine = create_engine(connectionString, echo = True)
    
    def connect(self):
        self.engine.connect()

    def dispose(self):
        self.engine.dispose()

    def createSchema(self):
        Base.metadata.create_all(self.engine)

    def insertTestRun(self, testRun):
        Session = sessionmaker(bind = self.engine)
        session = Session()
        session.add(testRun)
        session.commit()

    def insertTestRuns(self, testRuns):
        Session = sessionmaker(bind = self.engine)
        session = Session()

        for testRun in testRuns:
            session.add(testRun)

        session.commit()

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
