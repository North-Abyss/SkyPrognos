"""Smoke tests to ensure all modules import correctly."""


def test_imports():
    """Verify that main modules can be imported."""
    import prognos
    import prognos.data
    import prognos.features
    import prognos.models

    assert prognos.__name__ == "prognos"
