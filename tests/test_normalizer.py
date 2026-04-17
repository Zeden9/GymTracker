from datetime import datetime

from src.etl.normalizer import normalize_entry

entry1 = {
    "date": datetime(2024, 5, 2),
    "data": "ławka L 10x25 7kgx50,wyciąg pionowy 40kgx10 45x8",
}
print(normalize_entry(entry1["date"], entry1["data"]))


def test_normalize_entry():
    entry = {
        "date": datetime(2024, 5, 2),
        "data": "ława 10x25 7x50kg,wyciąg pionowy 40kgx10 45x8",
    }
    result = normalize_entry(entry["date"], entry["data"])

    assert len(result) == 4
    assert result[0]["Date"] == datetime(2024, 5, 2)
    assert result[0]["Exercise"] == "ława"
    assert result[0]["Set_Number"] == 1
    assert result[0]["Reps"] == 10
    assert result[0]["Weight"] == 25
    assert result[1]["Set_Number"] == 2
    assert result[1]["Reps"] == 7
    assert result[1]["Weight"] == 50
    assert result[2]["Exercise"] == "wyciąg pionowy"
    assert result[2]["Set_Number"] == 1
    assert result[2]["Reps"] == 10
    assert result[2]["Weight"] == 40
    assert result[3]["Set_Number"] == 2
    assert result[3]["Reps"] == 8
    assert result[3]["Weight"] == 45
