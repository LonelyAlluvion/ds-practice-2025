from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
<<<<<<< HEAD
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
=======
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)

DESCRIPTOR: _descriptor.FileDescriptor

class FraudRequest(_message.Message):
<<<<<<< HEAD
    __slots__ = ("order_id", "user_id", "amount", "shipping_method", "user_comment", "gift_wrapping", "country", "timestamp", "billing_address")
=======
    __slots__ = ("order_id", "user_id", "amount", "shipping_method", "user_comment", "gift_wrapping", "country", "timestamp", "billing_address", "vector_clock")
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    SHIPPING_METHOD_FIELD_NUMBER: _ClassVar[int]
    USER_COMMENT_FIELD_NUMBER: _ClassVar[int]
    GIFT_WRAPPING_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    BILLING_ADDRESS_FIELD_NUMBER: _ClassVar[int]
<<<<<<< HEAD
=======
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
    order_id: str
    user_id: str
    amount: float
    shipping_method: str
    user_comment: str
    gift_wrapping: bool
    country: str
    timestamp: int
    billing_address: BillingAddress
<<<<<<< HEAD
    def __init__(self, order_id: _Optional[str] = ..., user_id: _Optional[str] = ..., amount: _Optional[float] = ..., shipping_method: _Optional[str] = ..., user_comment: _Optional[str] = ..., gift_wrapping: bool = ..., country: _Optional[str] = ..., timestamp: _Optional[int] = ..., billing_address: _Optional[_Union[BillingAddress, _Mapping]] = ...) -> None: ...
=======
    vector_clock: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, order_id: _Optional[str] = ..., user_id: _Optional[str] = ..., amount: _Optional[float] = ..., shipping_method: _Optional[str] = ..., user_comment: _Optional[str] = ..., gift_wrapping: bool = ..., country: _Optional[str] = ..., timestamp: _Optional[int] = ..., billing_address: _Optional[_Union[BillingAddress, _Mapping]] = ..., vector_clock: _Optional[_Iterable[int]] = ...) -> None: ...
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)

class BillingAddress(_message.Message):
    __slots__ = ("street", "city", "state", "zip", "country")
    STREET_FIELD_NUMBER: _ClassVar[int]
    CITY_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    ZIP_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    street: str
    city: str
    state: str
    zip: str
    country: str
    def __init__(self, street: _Optional[str] = ..., city: _Optional[str] = ..., state: _Optional[str] = ..., zip: _Optional[str] = ..., country: _Optional[str] = ...) -> None: ...

class FraudResponse(_message.Message):
<<<<<<< HEAD
    __slots__ = ("flagged", "reason", "details")
    FLAGGED_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    flagged: bool
    reason: str
    details: FraudCheckDetails
    def __init__(self, flagged: bool = ..., reason: _Optional[str] = ..., details: _Optional[_Union[FraudCheckDetails, _Mapping]] = ...) -> None: ...
=======
    __slots__ = ("flagged", "reason", "details", "vector_clock")
    FLAGGED_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
    flagged: bool
    reason: str
    details: FraudCheckDetails
    vector_clock: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, flagged: bool = ..., reason: _Optional[str] = ..., details: _Optional[_Union[FraudCheckDetails, _Mapping]] = ..., vector_clock: _Optional[_Iterable[int]] = ...) -> None: ...
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)

class FraudCheckDetails(_message.Message):
    __slots__ = ("order_id", "status", "billing_address", "user_comment", "gift_wrapping", "shipping_method")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    BILLING_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    USER_COMMENT_FIELD_NUMBER: _ClassVar[int]
    GIFT_WRAPPING_FIELD_NUMBER: _ClassVar[int]
    SHIPPING_METHOD_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    status: str
    billing_address: BillingAddress
    user_comment: str
    gift_wrapping: bool
    shipping_method: str
    def __init__(self, order_id: _Optional[str] = ..., status: _Optional[str] = ..., billing_address: _Optional[_Union[BillingAddress, _Mapping]] = ..., user_comment: _Optional[str] = ..., gift_wrapping: bool = ..., shipping_method: _Optional[str] = ...) -> None: ...
<<<<<<< HEAD
=======

class ClearOrderRequest(_message.Message):
    __slots__ = ("order_id", "vector_clock")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    vector_clock: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, order_id: _Optional[str] = ..., vector_clock: _Optional[_Iterable[int]] = ...) -> None: ...

class ClearOrderResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
