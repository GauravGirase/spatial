## Threads
Threads are lightweight units of execution within a process.
They allow a program to perform multiple tasks at the same time (concurrently) within the same application.
A thread:
- Is the smallest unit of execution managed by a CPU
- Exists inside a process
- Shares memory and resources with other threads in the same process
- Runs independently but cooperatively with other threads

### Real-World Examples
- Web servers handling thousands of users
- Games rendering graphics while processing input
- Mobile apps downloading data in the background
```bash
import threading

def task():
    print("Thread running")

t = threading.Thread(target=task)
t.start()
```
