from junit import loadJunitTestRuns

junitDatabase = None

def import_junit(junit):
    testRuns = loadJunitTestRuns(junit)
    junitDatabase.insertTestRuns(testRuns)
    return len(testRuns), 201

def health():
    return "ok"
