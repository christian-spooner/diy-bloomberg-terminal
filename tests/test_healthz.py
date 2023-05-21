def health_check():
    return "ok"


def test_health_check():
    assert health_check() == "ok"
