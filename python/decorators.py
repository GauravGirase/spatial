# Basic implemetation 
from functools import wraps


def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Inside decorator")
        result = func(*args, **kwargs)
        return result*2
    return wrapper


@decorator
def add(a,b):
    return a+b

print(add(5,5))

