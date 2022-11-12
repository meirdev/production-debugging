from abc import ABC
from typing import Generic, List, NewType, Optional, TypeVar

from ..settings import Settings


Condition = NewType("Condition", str)


class BaseBreakpoint(ABC):
    @property
    def id(self) -> int:
        raise NotImplemented


BreakpointType = TypeVar("BreakpointType", bound=BaseBreakpoint)


class BaseDebugger(Generic[BreakpointType], ABC):
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def clear(self, *bp: BreakpointType) -> None:
        raise NotImplementedError

    def condition(
        self, bp: BreakpointType, condition: Optional[Condition] = None
    ) -> None:
        raise NotImplementedError

    def disable(self, *bp: BreakpointType) -> None:
        raise NotImplementedError

    def enable(self, *bp: BreakpointType) -> None:
        raise NotImplementedError

    def ignore(self, bp: BreakpointType, count: int = 0) -> None:
        raise NotImplementedError

    def list_break(self) -> List[BreakpointType]:
        raise NotImplementedError

    def set_break(
        self, filename: str, line_no: int, condition: Optional[Condition] = None
    ) -> BreakpointType:
        raise NotImplementedError

    def set_temp_break(
        self, filename: str, line_no: int, condition: Optional[Condition] = None
    ) -> BreakpointType:
        raise NotImplementedError
