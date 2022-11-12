import sys
from functools import cached_property
from types import FrameType
from typing import Any, Dict, List, Optional

from ..settings import Settings
from .base import BaseBreakpoint, BaseDebugger, Condition


class Breakpoint(BaseBreakpoint):
    def __init__(
        self,
        filename: str,
        line_no: int,
        condition: Optional[Condition] = None,
        temp: bool = False,
    ) -> None:
        super().__init__()

        self._filename = filename
        self._line_no = line_no
        self._condition = condition
        self._temp = temp

        self._enabled = True
        self._ignore = 0
        self._hits = 0

    @property
    def id(self) -> int:
        return id(self)

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def line_no(self) -> int:
        return self._line_no

    @cached_property
    def compiled_condition(self) -> Any:
        if self._condition is None:
            return None
        return compile(self._condition, "<string>", "eval")

    @property
    def condition(self) -> Optional[Condition]:
        return self._condition

    @condition.setter
    def condition(self, value: Optional[Condition] = None) -> None:
        self._condition = value

        del self.__dict__["compiled_condition"]

    @property
    def enabled(self) -> bool:
        return self._enabled

    def enable(self) -> None:
        self._enabled = True

    def disable(self) -> None:
        self._enabled = False

    @property
    def temp(self) -> bool:
        return self._temp

    @property
    def ignore(self) -> int:
        return self._ignore

    @ignore.setter
    def ignore(self, value: int) -> None:
        self._ignore = value

    def dec_ignore(self) -> None:
        self._ignore -= 1

    @property
    def hits(self) -> int:
        return self._hits

    def inc_hits(self) -> None:
        self._hits += 1


class Trace(BaseDebugger[Breakpoint]):
    def __init__(self, settings: Settings) -> None:
        super().__init__(settings)

        self._breakpoints: Dict[int, Breakpoint] = {}

        sys.settrace(self._trace_function)

    def _trace_function(self, frame: FrameType, event: str, arg: Any):
        filename, line_no = frame.f_code.co_filename, frame.f_lineno

        breakpoints = list(self._breakpoints.values())
        for breakpoint in breakpoints:
            if (
                breakpoint.enabled
                and line_no == breakpoint.line_no
                and filename == str(self._settings.root / breakpoint.filename)
            ):
                if breakpoint.compiled_condition is not None:
                    condition = eval(
                        breakpoint.compiled_condition, frame.f_globals, frame.f_locals
                    )
                    if not condition:
                        continue

                if breakpoint.ignore > 0:
                    breakpoint.dec_ignore()
                    continue

                self._settings.callback(breakpoint.id, frame)

                breakpoint.inc_hits()

                if breakpoint.temp:
                    self.clear(breakpoint)

        return self._trace_function

    def clear(self, *bp: Breakpoint) -> None:
        if len(bp) == 0:
            bp = tuple(self._breakpoints.values())

        for bp_ in bp:
            self._breakpoints.pop(bp_.id)

    def condition(self, bp: Breakpoint, condition: Optional[Condition] = None) -> None:
        bp.condition = condition

    def disable(self, *bp: Breakpoint) -> None:
        for bp_ in bp:
            bp_.disable()

    def enable(self, *bp: Breakpoint) -> None:
        for bp_ in bp:
            bp_.enable()

    def ignore(self, bp: Breakpoint, count: int = 0) -> None:
        bp.ignore = count

    def list_break(self) -> List[Breakpoint]:
        return list(self._breakpoints.values())

    def set_break(
        self, filename: str, line_no: int, condition: Optional[Condition] = None
    ) -> Breakpoint:
        breakpoint = Breakpoint(filename, line_no, condition)
        self._breakpoints[breakpoint.id] = breakpoint
        return breakpoint

    def set_temp_break(
        self, filename: str, line_no: int, condition: Optional[Condition] = None
    ) -> Breakpoint:
        breakpoint = Breakpoint(filename, line_no, condition, True)
        self._breakpoints[breakpoint.id] = breakpoint
        return breakpoint

    def __del__(self) -> None:
        sys.settrace(None)
