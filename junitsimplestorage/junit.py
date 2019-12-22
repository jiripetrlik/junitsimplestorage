from junitparser import JUnitXml, TestSuite
from junitsimplestorage.database import JunitTestRun
import xml.etree.ElementTree as ET
import datetime

TEST_STATUS_PASSED = "passed"

def loadJunitTestRuns(junitString):
    testSuite = TestSuite.fromstring(junitString)
    testCasesList = []

    root = ET.fromstring(junitString)
    rootElementName = root.tag.lower()
    if rootElementName == "testsuites":
        testCasesList = []
        xml = JUnitXml.fromelem(root)
        for testSuite in xml:
            testCasesList = testCasesList + importTestSuite(testSuite)

        return testCasesList
    elif rootElementName == "testsuite":
        testSuite = TestSuite.fromelem(root)
        return importTestSuite(testSuite)
    else:
        raise Exception("Unknown parent element for junit: " + rootElementName)

def importTestSuite(testSuite):
    testCasesList = []
    for item in testSuite:
        timestamp = testSuite.timestamp
        if timestamp is not None:
            timestamp = datetime.datetime.strptime(testSuite.timestamp, '%Y-%m-%dT%H:%M:%S.%f')

        testRun = JunitTestRun(
            testSuiteName = testSuite.name,
            timestamp = timestamp,
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
