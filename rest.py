from junit import loadJunitTestRuns

junitDatabase = None

def import_junit(junit):
    testRuns = loadJunitTestRuns(junit)
    testRunsIds = junitDatabase.insertTestRuns(testRuns)

    result = {
        "numberOfItems" : len(testRunsIds),
        "ids" : testRunsIds
    }
    return result, 201

def health():
    return "Ready!"
