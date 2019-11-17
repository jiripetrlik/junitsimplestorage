from junitparser import JUnitXml
from database import JunitTestRun
import datetime

TEST_STATUS_PASSED = "passed"

def loadJunitTestRuns(junitString):
    xml = JUnitXml.fromstring(junitString)
    testCasesList = []
    for testSuite in xml:
        for item in testSuite:
            testRun = JunitTestRun(
                testSuiteName = testSuite.name,
                timestamp = datetime.datetime.strptime(testSuite.timestamp, '%Y-%m-%dT%H:%M:%S.%f'),
                hostname = testSuite.hostname,
                name = item.name,
                classname = item.classname,
                time = item.time,
                state = testRunState(item),
                message = testRunMessage(item)
            )
            
            testCasesList.append(testRun)

    return testCasesList

def testRunState(item):
    if item.result is None:
        return TEST_STATUS_PASSED
    else:
        return item.result._tag

def testRunMessage(item):
    if item.result is None:
        return None
    else:
        return item.result.message
