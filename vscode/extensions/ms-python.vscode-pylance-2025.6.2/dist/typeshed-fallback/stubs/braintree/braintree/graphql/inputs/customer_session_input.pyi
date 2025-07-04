from _typeshed import Incomplete
from typing_extensions import Self

from braintree.graphql.inputs.phone_input import PhoneInput

class CustomerSessionInput:
    def __init__(
        self,
        email: str | None = None,
        hashed_email: str | None = None,
        phone: PhoneInput | None = None,
        hashed_phone_number: str | None = None,
        device_fingerprint_id: str | None = None,
        paypal_app_installed: bool | None = None,
        venmo_app_installed: bool | None = None,
        user_agent: str | None = None,
    ) -> None: ...
    def to_graphql_variables(self) -> dict[str, Incomplete]: ...
    @staticmethod
    def builder() -> Builder: ...

    class Builder:
        def __init__(self) -> None: ...
        def email(self, email: str) -> Self: ...
        def hashed_email(self, hashed_email: str) -> Self: ...
        def phone(self, phone: PhoneInput) -> Self: ...
        def hashed_phone_number(self, hashed_phone_number: str) -> Self: ...
        def device_fingerprint_id(self, device_fingerprint_id: str) -> Self: ...
        def paypal_app_installed(self, paypal_app_installed: bool) -> Self: ...
        def venmo_app_installed(self, venmo_app_installed: bool) -> Self: ...
        def user_agent(self, user_agent: str) -> Self: ...
        def build(self) -> CustomerSessionInput: ...
