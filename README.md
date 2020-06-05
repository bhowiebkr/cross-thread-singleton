# python-process-lock
A locking mechanism for a python process. Should be cross platform safe.


See the main.py:

```python
from locker import locker

@locker
def main():
    print("\nHello World!")
```
