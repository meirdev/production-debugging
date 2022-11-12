from dataclasses import dataclass
from pathlib import Path
from types import FrameType
from typing import Callable

BreakpointId = int


@dataclass
class Settings:
    root: Path
    callback: Callable[[BreakpointId, FrameType], None]
