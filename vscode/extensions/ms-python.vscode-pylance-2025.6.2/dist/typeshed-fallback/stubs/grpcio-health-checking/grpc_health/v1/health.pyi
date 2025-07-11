from _typeshed import Incomplete
from collections.abc import Callable
from concurrent import futures
from typing import Final, overload
from typing_extensions import Self

from grpc import ServicerContext
from grpc_health.v1 import health_pb2, health_pb2_grpc

SERVICE_NAME: Final[str]
OVERALL_HEALTH: Final[str]

class _Watcher:
    def __init__(self) -> None: ...
    def __iter__(self) -> Self: ...
    def next(self) -> health_pb2.HealthCheckResponse: ...
    def __next__(self) -> health_pb2.HealthCheckResponse: ...
    def add(self, response: health_pb2.HealthCheckResponse) -> None: ...
    def close(self) -> None: ...

class HealthServicer(health_pb2_grpc.HealthServicer):
    def __init__(
        self, experimental_non_blocking: bool = True, experimental_thread_pool: futures.ThreadPoolExecutor | None = None
    ) -> None: ...
    def Check(self, request: health_pb2.HealthCheckRequest, context: ServicerContext) -> health_pb2.HealthCheckResponse: ...
    @overload
    def Watch(
        self, request: health_pb2.HealthCheckRequest, context: ServicerContext, send_response_callback: None = None
    ) -> _Watcher: ...
    @overload
    def Watch(
        self, request: health_pb2.HealthCheckRequest, context: ServicerContext, send_response_callback: Callable[..., Incomplete]
    ) -> None: ...
    def set(self, service: str, status: health_pb2.HealthCheckResponse.ServingStatus) -> None: ...
    def enter_graceful_shutdown(self) -> None: ...
