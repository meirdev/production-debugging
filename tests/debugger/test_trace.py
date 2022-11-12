from pathlib import Path
from unittest.mock import Mock

from production_debugging.debugger.trace import Trace
from production_debugging.settings import Settings


def foo():
    i = 1
    j = 2
    print(i + j)


def callback(id, frame):
    print("locals", frame.f_locals)


def test_trace():
    mock = Mock()
    mock.side_effect = callback

    settings = Settings(root=Path("/workspaces/production-debugging"), callback=mock)

    trace = Trace(settings)
    bp = trace.set_break("tests/debugger/test_trace.py", 10, "i < 2")

    foo()

    assert mock.call_count == 1

    trace.disable(bp)

    foo()

    assert mock.call_count == 1

    trace.enable(bp)

    foo()

    assert mock.call_count == 2

    assert trace.list_break() == [bp]

    trace.ignore(bp, 2)

    foo()
    foo()
    foo()

    assert mock.call_count == 3

    trace.clear()

    foo()

    assert mock.call_count == 3
