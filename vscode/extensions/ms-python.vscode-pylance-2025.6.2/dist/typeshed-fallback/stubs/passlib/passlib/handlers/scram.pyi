from _typeshed import Incomplete
from typing import ClassVar
from typing_extensions import Self

import passlib.utils.handlers as uh

class scram(uh.HasRounds, uh.HasRawSalt, uh.HasRawChecksum, uh.GenericHandler):  # type: ignore[misc]
    name: ClassVar[str]
    ident: ClassVar[str]
    default_salt_size: ClassVar[int]
    max_salt_size: ClassVar[int]
    default_rounds: ClassVar[int]
    min_rounds: ClassVar[int]
    max_rounds: ClassVar[int]
    rounds_cost: ClassVar[str]
    default_algs: ClassVar[list[str]]
    algs: Incomplete | None
    @classmethod
    def extract_digest_info(cls, hash, alg): ...
    @classmethod
    def extract_digest_algs(cls, hash, format: str = "iana"): ...
    @classmethod
    def derive_digest(cls, password, salt, rounds, alg): ...
    @classmethod
    def from_string(cls, hash) -> Self: ...  # type: ignore[override]
    @classmethod
    def using(cls, default_algs=None, algs=None, **kwds): ...  # type: ignore[override]
    def __init__(self, algs=None, **kwds) -> None: ...
    @classmethod
    def verify(cls, secret, hash, full: bool = False): ...  # type: ignore[override]

__all__ = ["scram"]
