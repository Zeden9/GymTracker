from datetime import datetime

from src.parser import parse_workout_text


def test_simple_set():
    text = """
    02.05.2024
    ława
    10x15 20kgx15 25kgx10
    Iso curl
    12x12 13x10 15kgx8"""
    result = parse_workout_text(text)

    assert len(result) == 1
    assert result[0]["date"] == datetime(2024, 5, 2)
    assert result[0]["data"] == "ława 10x15 20kgx15 25kgx10,Iso curl 12x12 13x10 15kgx8"
