# Decorators
## 1. Logging (very common)
```bash
from functools import wraps

def log_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with {args}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper


@log_decorator
def add(a, b):
    return a + b
```
## 2. Authentication / Authorization
```bash
def login_required(func):
    @wraps(func)
    def wrapper(user, *args, **kwargs):
        if not user.get("is_logged_in"):
            return "Access denied"
        return func(user, *args, **kwargs)
    return wrapper


@login_required
def dashboard(user):
    return "Welcome to dashboard"
```
## 3. Performance Timing
```bash
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"Time: {time.time() - start}")
        return result
    return wrapper
```
## 4. Retry Logic (fault tolerance)
```bash
import time

def retry(func):
    def wrapper(*args, **kwargs):
        for _ in range(3):
            try:
                return func(*args, **kwargs)
            except Exception:
                time.sleep(1)
        return "Failed after retries"
    return wrapper
```
## 5. Input Validation
```bash
def validate_positive(func):
    def wrapper(x):
        if x < 0:
            raise ValueError("Must be positive")
        return func(x)
    return wrapper
```
## 6. Transactions (Database)
```bash
def transaction(func):
    def wrapper(*args, **kwargs):
        print("Start transaction")
        result = func(*args, **kwargs)
        print("Commit transaction")
        return result
    return wrapper
```
