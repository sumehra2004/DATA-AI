def decorator(func):
    def wrapper(*args, **kwargs):
        print("Before function execution")
        result = func(*args, **kwargs)
        print("After function execution")
        return result
    return wrapper
@decorator
def add(x, y):
    return x + y
print(add(5, 3))