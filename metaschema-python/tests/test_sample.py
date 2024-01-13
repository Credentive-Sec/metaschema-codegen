# Simple test to make sure the pytest environment is correctly configured
def hello_string(s: str) -> str:
    return f"Hello, {s}!"


def test_sample():
    assert hello_string("World") == "Hello, World!"
