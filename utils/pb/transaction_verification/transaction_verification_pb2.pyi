<<<<<<< HEAD
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
=======
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)

DESCRIPTOR: _descriptor.FileDescriptor

class TransactionRequest(_message.Message):
<<<<<<< HEAD
    __slots__ = ("order_id", "user_id", "amount", "credit_card", "discount_code", "billing_address", "shipping_method", "user_comment", "gift_wrapping")
=======
    __slots__ = ("order_id", "user_id", "amount", "credit_card", "discount_code", "billing_address", "shipping_method", "user_comment", "gift_wrapping", "vector_clock")
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    CREDIT_CARD_FIELD_NUMBER: _ClassVar[int]
    DISCOUNT_CODE_FIELD_NUMBER: _ClassVar[int]
    BILLING_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SHIPPING_METHOD_FIELD_NUMBER: _ClassVar[int]
    USER_COMMENT_FIELD_NUMBER: _ClassVar[int]
    GIFT_WRAPPING_FIELD_NUMBER: _ClassVar[int]
<<<<<<< HEAD
=======
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
    order_id: str
    user_id: str
    amount: float
    credit_card: CreditCard
    discount_code: str
    billing_address: BillingAddress
    shipping_method: str
    user_comment: str
    gift_wrapping: bool
<<<<<<< HEAD
    def __init__(self, order_id: _Optional[str] = ..., user_id: _Optional[str] = ..., amount: _Optional[float] = ..., credit_card: _Optional[_Union[CreditCard, _Mapping]] = ..., discount_code: _Optional[str] = ..., billing_address: _Optional[_Union[BillingAddress, _Mapping]] = ..., shipping_method: _Optional[str] = ..., user_comment: _Optional[str] = ..., gift_wrapping: bool = ...) -> None: ...
=======
    vector_clock: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, order_id: _Optional[str] = ..., user_id: _Optional[str] = ..., amount: _Optional[float] = ..., credit_card: _Optional[_Union[CreditCard, _Mapping]] = ..., discount_code: _Optional[str] = ..., billing_address: _Optional[_Union[BillingAddress, _Mapping]] = ..., shipping_method: _Optional[str] = ..., user_comment: _Optional[str] = ..., gift_wrapping: bool = ..., vector_clock: _Optional[_Iterable[int]] = ...) -> None: ...
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)

class CreditCard(_message.Message):
    __slots__ = ("number", "expiration_date", "cvv")
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_DATE_FIELD_NUMBER: _ClassVar[int]
    CVV_FIELD_NUMBER: _ClassVar[int]
    number: str
    expiration_date: str
    cvv: str
    def __init__(self, number: _Optional[str] = ..., expiration_date: _Optional[str] = ..., cvv: _Optional[str] = ...) -> None: ...

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

class TransactionResponse(_message.Message):
<<<<<<< HEAD
    __slots__ = ("approved", "reason", "details")
    APPROVED_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    approved: bool
    reason: str
    details: TransactionDetails
    def __init__(self, approved: bool = ..., reason: _Optional[str] = ..., details: _Optional[_Union[TransactionDetails, _Mapping]] = ...) -> None: ...
=======
    __slots__ = ("approved", "reason", "details", "vector_clock")
    APPROVED_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
    approved: bool
    reason: str
    details: TransactionDetails
    vector_clock: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, approved: bool = ..., reason: _Optional[str] = ..., details: _Optional[_Union[TransactionDetails, _Mapping]] = ..., vector_clock: _Optional[_Iterable[int]] = ...) -> None: ...
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)

class TransactionDetails(_message.Message):
    __slots__ = ("order_id", "status", "billing_address", "discount_code", "charged_amount", "shipping_method", "user_comment", "gift_wrapping")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    BILLING_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    DISCOUNT_CODE_FIELD_NUMBER: _ClassVar[int]
    CHARGED_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    SHIPPING_METHOD_FIELD_NUMBER: _ClassVar[int]
    USER_COMMENT_FIELD_NUMBER: _ClassVar[int]
    GIFT_WRAPPING_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    status: str
    billing_address: BillingAddress
    discount_code: str
    charged_amount: float
    shipping_method: str
    user_comment: str
    gift_wrapping: bool
    def __init__(self, order_id: _Optional[str] = ..., status: _Optional[str] = ..., billing_address: _Optional[_Union[BillingAddress, _Mapping]] = ..., discount_code: _Optional[str] = ..., charged_amount: _Optional[float] = ..., shipping_method: _Optional[str] = ..., user_comment: _Optional[str] = ..., gift_wrapping: bool = ...) -> None: ...
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
