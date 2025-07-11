from _typeshed import Incomplete

from braintree.error_result import ErrorResult
from braintree.successful_result import SuccessfulResult

class ApplePayGateway:
    gateway: Incomplete
    config: Incomplete
    def __init__(self, gateway) -> None: ...
    def register_domain(self, domain: str) -> SuccessfulResult | ErrorResult | None: ...
    def unregister_domain(self, domain: str) -> SuccessfulResult: ...
    def registered_domains(self): ...
