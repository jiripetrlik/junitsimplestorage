from junitsimplestorage.junit import loadJunitTestRuns

def test_import(exampleJunitString):
    testRuns = loadJunitTestRuns(exampleJunitString)
    assert len(testRuns) > 0
