import sys
from typing import Any, Literal
from typing_extensions import Self, TypeAlias

from sympy.polys.domains.domain import Domain
from sympy.polys.domains.domainelement import DomainElement
from sympy.printing.defaults import DefaultPrinting

if sys.version_info >= (3, 10):
    from types import NotImplementedType
else:
    NotImplementedType: TypeAlias = Any

class ExtensionElement(DomainElement, DefaultPrinting):  # type: ignore
    __slots__ = ...
    def __init__(self, rep, ext) -> None: ...
    def parent(self) -> Any: ...
    def __bool__(self) -> bool: ...
    def __pos__(self) -> Self: ...
    def __neg__(self) -> ExtElem: ...
    def __add__(self, g) -> ExtElem | NotImplementedType: ...

    __radd__ = ...
    def __sub__(self, g) -> ExtElem | NotImplementedType: ...
    def __rsub__(self, g) -> ExtElem | NotImplementedType: ...
    def __mul__(self, g) -> ExtElem | NotImplementedType: ...

    __rmul__ = ...
    def inverse(self) -> ExtElem: ...
    def __truediv__(self, g) -> NotImplementedType | ExtElem: ...

    __floordiv__ = ...
    def __rtruediv__(self, g) -> NotImplementedType: ...

    __rfloordiv__ = ...
    def __mod__(self, g) -> NotImplementedType: ...
    def __rmod__(self, g) -> NotImplementedType: ...
    def __pow__(self, n) -> ExtElem: ...
    def __eq__(self, g) -> bool: ...
    def __ne__(self, g) -> bool: ...
    def __hash__(self) -> int: ...

    __repr__ = ...
    @property
    def is_ground(f): ...
    def to_ground(self): ...

ExtElem = ExtensionElement

class MonogenicFiniteExtension(Domain):  # type: ignore
    is_FiniteExtension = ...
    dtype = ExtensionElement
    def __init__(self, mod) -> None: ...
    def new(self, arg) -> ExtElem: ...
    def __eq__(self, other) -> bool: ...
    def __hash__(self) -> int: ...

    __repr__ = ...
    def convert(self, f, base=...) -> ExtElem: ...
    def convert_from(self, f, base) -> ExtElem: ...
    def to_sympy(self, f): ...
    def from_sympy(self, f) -> ExtElem: ...
    def set_domain(self, K) -> Self: ...
    def drop(self, *symbols) -> Self: ...
    def quo(self, f, g) -> ExtElem: ...
    def exquo(self, f, g) -> ExtElem: ...
    def is_negative(self, a) -> Literal[False]: ...
    def is_unit(self, a) -> bool | None: ...

FiniteExtension = MonogenicFiniteExtension
