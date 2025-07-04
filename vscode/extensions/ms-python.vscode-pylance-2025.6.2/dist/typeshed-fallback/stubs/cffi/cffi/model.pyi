from _thread import LockType
from _typeshed import Incomplete
from collections.abc import Generator
from typing import Final

from .error import CDefError as CDefError, VerificationError as VerificationError, VerificationMissing as VerificationMissing
from .lock import allocate_lock as allocate_lock

Q_CONST: Final = 1
Q_RESTRICT: Final = 2
Q_VOLATILE: Final = 4

def qualify(quals: int, replace_with: str) -> str: ...

class BaseTypeByIdentity:
    is_array_type: bool
    is_raw_function: bool
    def get_c_name(self, replace_with: str = "", context: str = "a C file", quals: int = 0) -> str: ...
    def has_c_name(self) -> bool: ...
    def is_integer_type(self) -> bool: ...
    def get_cached_btype(self, ffi, finishlist, can_delay: bool = False): ...

class BaseType(BaseTypeByIdentity):
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...

class VoidType(BaseType):
    c_name_with_marker: str
    def __init__(self) -> None: ...
    def build_backend_type(self, ffi, finishlist): ...

void_type: VoidType

class BasePrimitiveType(BaseType):
    def is_complex_type(self) -> bool: ...

class PrimitiveType(BasePrimitiveType):
    ALL_PRIMITIVE_TYPES: dict[str, str]
    name: str
    c_name_with_marker: str
    def __init__(self, name: str) -> None: ...
    def is_char_type(self) -> bool: ...
    def is_integer_type(self) -> bool: ...
    def is_float_type(self) -> bool: ...
    def is_complex_type(self) -> bool: ...
    def build_backend_type(self, ffi, finishlist): ...

class UnknownIntegerType(BasePrimitiveType):
    name: str
    c_name_with_marker: str
    def __init__(self, name: str) -> None: ...
    def is_integer_type(self) -> bool: ...
    def build_backend_type(self, ffi, finishlist) -> None: ...

class UnknownFloatType(BasePrimitiveType):
    name: str
    c_name_with_marker: str
    def __init__(self, name: str) -> None: ...
    def build_backend_type(self, ffi, finishlist) -> None: ...

class BaseFunctionType(BaseType):
    args: Incomplete
    result: Incomplete
    ellipsis: Incomplete
    abi: Incomplete
    c_name_with_marker: str
    def __init__(self, args, result, ellipsis, abi=None) -> None: ...

class RawFunctionType(BaseFunctionType):
    is_raw_function: bool
    def build_backend_type(self, ffi, finishlist) -> None: ...
    def as_function_pointer(self) -> FunctionPtrType: ...

class FunctionPtrType(BaseFunctionType):
    def build_backend_type(self, ffi, finishlist): ...
    def as_raw_function(self) -> RawFunctionType: ...

class PointerType(BaseType):
    totype: BaseTypeByIdentity
    quals: int
    c_name_with_marker: str
    def __init__(self, totype: BaseTypeByIdentity, quals: int = 0) -> None: ...
    def build_backend_type(self, ffi, finishlist): ...

voidp_type: PointerType

def ConstPointerType(totype: BaseTypeByIdentity) -> PointerType: ...

const_voidp_type: PointerType

class NamedPointerType(PointerType):
    name: str
    c_name_with_marker: str
    def __init__(self, totype: BaseTypeByIdentity, name: str, quals: int = 0) -> None: ...

class ArrayType(BaseType):
    is_array_type: bool
    item: Incomplete
    length: str | None
    c_name_with_marker: str
    def __init__(self, item, length: str | None) -> None: ...
    def length_is_unknown(self) -> bool: ...
    def resolve_length(self, newlength: str | None) -> ArrayType: ...
    def build_backend_type(self, ffi, finishlist): ...

char_array_type: ArrayType

class StructOrUnionOrEnum(BaseTypeByIdentity):
    forcename: str | None
    c_name_with_marker: str
    def build_c_name_with_marker(self) -> None: ...
    def force_the_name(self, forcename: str | None) -> None: ...
    def get_official_name(self) -> str: ...

class StructOrUnion(StructOrUnionOrEnum):
    fixedlayout: Incomplete
    completed: int
    partial: bool
    packed: int
    name: Incomplete
    fldnames: Incomplete
    fldtypes: Incomplete
    fldbitsize: Incomplete
    fldquals: Incomplete
    def __init__(self, name, fldnames, fldtypes, fldbitsize, fldquals=None) -> None: ...
    def anonymous_struct_fields(self) -> Generator[StructOrUnion, None, None]: ...
    def enumfields(self, expand_anonymous_struct_union: bool = True) -> Generator[Incomplete, None, None]: ...
    def force_flatten(self) -> None: ...
    def get_cached_btype(self, ffi, finishlist, can_delay: bool = False): ...
    def finish_backend_type(self, ffi, finishlist) -> None: ...
    def check_not_partial(self) -> None: ...
    def build_backend_type(self, ffi, finishlist): ...

class StructType(StructOrUnion):
    kind: str

class UnionType(StructOrUnion):
    kind: str

class EnumType(StructOrUnionOrEnum):
    kind: str
    partial: bool
    partial_resolved: bool
    name: Incomplete
    enumerators: Incomplete
    enumvalues: Incomplete
    baseinttype: Incomplete
    def __init__(self, name, enumerators, enumvalues, baseinttype=None) -> None: ...
    forcename: str | None
    def force_the_name(self, forcename: str | None) -> None: ...
    def check_not_partial(self) -> None: ...
    def build_backend_type(self, ffi, finishlist): ...
    def build_baseinttype(self, ffi, finishlist): ...

def unknown_type(name: str, structname: str | None = None) -> StructType: ...
def unknown_ptr_type(name: str, structname: str | None = None) -> NamedPointerType: ...

global_lock: LockType

def get_typecache(backend): ...
def global_cache(srctype, ffi, funcname, *args, **kwds): ...
def pointer_cache(ffi, BType): ...
def attach_exception_info(e, name: str) -> None: ...
