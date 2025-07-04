import os
import sys
from _typeshed import BytesPath, FileDescriptorOrPath, StrOrBytesPath, StrPath, SupportsRichComparisonT
from collections.abc import Sequence
from typing import Literal, NewType, overload
from typing_extensions import LiteralString

__all__ = [
    "commonprefix",
    "exists",
    "getatime",
    "getctime",
    "getmtime",
    "getsize",
    "isdir",
    "isfile",
    "samefile",
    "sameopenfile",
    "samestat",
    "ALLOW_MISSING",
]
if sys.version_info >= (3, 12):
    __all__ += ["islink"]
if sys.version_info >= (3, 13):
    __all__ += ["isjunction", "isdevdrive", "lexists"]

# All overloads can return empty string. Ideally, Literal[""] would be a valid
# Iterable[T], so that list[T] | Literal[""] could be used as a return
# type. But because this only works when T is str, we need Sequence[T] instead.
@overload
def commonprefix(m: Sequence[LiteralString]) -> LiteralString: ...
@overload
def commonprefix(m: Sequence[StrPath]) -> str: ...
@overload
def commonprefix(m: Sequence[BytesPath]) -> bytes | Literal[""]: ...
@overload
def commonprefix(m: Sequence[list[SupportsRichComparisonT]]) -> Sequence[SupportsRichComparisonT]: ...
@overload
def commonprefix(m: Sequence[tuple[SupportsRichComparisonT, ...]]) -> Sequence[SupportsRichComparisonT]: ...
def exists(path: FileDescriptorOrPath) -> bool: ...
def getsize(filename: FileDescriptorOrPath) -> int: ...
def isfile(path: FileDescriptorOrPath) -> bool: ...
def isdir(s: FileDescriptorOrPath) -> bool: ...

if sys.version_info >= (3, 12):
    def islink(path: StrOrBytesPath) -> bool: ...

# These return float if os.stat_float_times() == True,
# but int is a subclass of float.
def getatime(filename: FileDescriptorOrPath) -> float: ...
def getmtime(filename: FileDescriptorOrPath) -> float: ...
def getctime(filename: FileDescriptorOrPath) -> float: ...
def samefile(f1: FileDescriptorOrPath, f2: FileDescriptorOrPath) -> bool: ...
def sameopenfile(fp1: int, fp2: int) -> bool: ...
def samestat(s1: os.stat_result, s2: os.stat_result) -> bool: ...

if sys.version_info >= (3, 13):
    def isjunction(path: StrOrBytesPath) -> bool: ...
    def isdevdrive(path: StrOrBytesPath) -> bool: ...
    def lexists(path: StrOrBytesPath) -> bool: ...

# Added in Python 3.9.23, 3.10.18, 3.11.13, 3.12.11, 3.13.4
_AllowMissingType = NewType("_AllowMissingType", object)
ALLOW_MISSING: _AllowMissingType
