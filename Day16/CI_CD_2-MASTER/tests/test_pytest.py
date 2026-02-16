from app.calculator import add, subtract, get_api_status

def test_add():
    assert add(2, 3) == 5

def test_subtract():
    assert subtract(5, 3) == 2

def test_api():
    assert get_api_status() == 200
