# Production debugging

Debugging with non-breaking breakpoints.

## Example

`add.py`:

```python
def add(x, y) -> int:
    sum = x + y
    return sum
```

`debug.py`:

```python
from pathlib import Path

from production_debugging.debugger.trace import Trace
from production_debugging.settings import Settings

from add import add


def callback(id, frame):
    print("locals", frame.f_locals)


settings = Settings(root=Path(__file__).absolute().parent, callback=callback)

trace = Trace(settings)
bp = trace.set_break("add.py", 2)

print(add(5, 6))
```

Output:

```text
locals {'x': 5, 'y': 6}
11
```
