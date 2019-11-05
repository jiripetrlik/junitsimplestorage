from junitparser import JUnitXml

def test_import():
    xml = JUnitXml.fromfile("tests/junit-report-example.xml")
    assert next(iter(xml)).name == "MyTestSuite"
