from rest import __parseLabels

def test_parse_labels_empty():
    str = ""
    labels = __parseLabels(str)
    assert len(labels) == 0

def test_parse_labels():
    str = "label1:value1,label2:value2,label3:value3"
    labels = __parseLabels(str)
    assert len(labels) == 3
    assert labels["label1"] == "value1"
    assert labels["label2"] == "value2"
    assert labels["label3"] == "value3"