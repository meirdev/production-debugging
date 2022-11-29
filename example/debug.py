import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from production_debugging.debugger.trace import Trace
from production_debugging.settings import Settings

from add import add


def callback(id, frame):
    print("locals", frame.f_locals)


settings = Settings(root=Path(__file__).absolute().parent, callback=callback)

trace = Trace(settings)
bp = trace.set_break("add.py", 2)

print(add(5, 6))
