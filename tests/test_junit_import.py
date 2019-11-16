from junit_simple_storage.junit import loadJunitTestRuns

def test_import():
    testRuns = loadJunitTestRuns("tests/junit-report-example.xml")
    assert len(testRuns) > 0
