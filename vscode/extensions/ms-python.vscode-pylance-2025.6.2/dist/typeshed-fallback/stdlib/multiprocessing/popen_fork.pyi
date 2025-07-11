import sys
from typing import ClassVar

from .process import BaseProcess
from .util import Finalize

if sys.platform != "win32":
    __all__ = ["Popen"]

    class Popen:
        finalizer: Finalize | None
        method: ClassVar[str]
        pid: int
        returncode: int | None
        sentinel: int  # doesn't exist if os.fork in _launch returns 0

        def __init__(self, process_obj: BaseProcess) -> None: ...
        def duplicate_for_child(self, fd: int) -> int: ...
        def poll(self, flag: int = 1) -> int | None: ...
        def wait(self, timeout: float | None = None) -> int | None: ...
        if sys.version_info >= (3, 14):
            def interrupt(self) -> None: ...

        def terminate(self) -> None: ...
        def kill(self) -> None: ...
        def close(self) -> None: ...
