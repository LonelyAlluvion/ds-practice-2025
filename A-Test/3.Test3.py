import time
import sys
import os
import grpc
from concurrent import futures

# === Import gRPC stubs ===
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
transaction_verification_grpc_path = os.path.abspath(os.path.join(FILE, '../../utils/pb/transaction_verification'))
sys.path.insert(0, transaction_verification_grpc_path)

import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc


def test_transaction_verification(order_id, user_id, amount, credit_card, discount_code, billing_address):
    with grpc.insecure_channel("localhost:50052") as channel:
        stub = transaction_verification_pb2_grpc.TransactionVerificationStub(channel)

<<<<<<< HEAD
        # Build the request object
=======
        # 构建请求对象
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
        request = transaction_verification.TransactionRequest(
            order_id=order_id,
            user_id=user_id,
            amount=amount,
            credit_card=credit_card,
            discount_code=discount_code,
            billing_address=transaction_verification.BillingAddress(
                street=billing_address["street"],
                city=billing_address["city"],
                state=billing_address["state"],
                zip=billing_address["zip"],
                country=billing_address["country"]
            )
        )

<<<<<<< HEAD
        # Send the request and get the response
        response = stub.VerifyTransaction(request)

        # Print the transaction verification result
=======
        # 发送请求并获取响应
        response = stub.VerifyTransaction(request)

        # 打印返回的验证结果
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
        print(f"Transaction Verification for Order {order_id}, User {user_id}:")
        print(f"Approved: {response.approved}, Reason: {response.reason}")
        print(f"Final Amount Charged: {response.details.charged_amount}")
        print(f"Discount Code: {response.details.discount_code}")
        print("===")


<<<<<<< HEAD
# ✅ Test 1: Valid credit card, correct CVV, and valid discount code
=======
# ✅ 测试 1：有效的信用卡，正确的 CVV 和有效的折扣码
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
test_transaction_verification(
    order_id="ORD-JohnDoe-1",
    user_id="user567",
    amount=100,
    credit_card=transaction_verification.CreditCard(
        number="4111111111111111",
        expiration_date="12/25",
        cvv="123"
    ),
    discount_code="SAVE10",
    billing_address={
        "street": "123 Main St",
        "city": "Springfield",
        "state": "IL",
        "zip": "62701",
        "country": "USA"
    }
)

<<<<<<< HEAD
# ❌ Test 2: Expired credit card
=======
# ❌ 测试 2：过期的信用卡
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
test_transaction_verification(
    order_id="ORD-JohnDoe-2",
    user_id="user789",
    amount=150,
    credit_card=transaction_verification.CreditCard(
        number="4111111111111111",
        expiration_date="12/20",
        cvv="456"
    ),
    discount_code="SAVE10",
    billing_address={
        "street": "456 Oak St",
        "city": "Chicago",
        "state": "IL",
        "zip": "60601",
        "country": "USA"
    }
)

<<<<<<< HEAD
# ❌ Test 3: Invalid CVV
=======
# ❌ 测试 3：无效的 CVV
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
test_transaction_verification(
    order_id="ORD-JaneDoe-3",
    user_id="user123",
    amount=200,
    credit_card=transaction_verification.CreditCard(
        number="4111111111111111",
        expiration_date="12/25",
        cvv="000"
    ),
    discount_code="VIP20",
    billing_address={
        "street": "789 Elm St",
        "city": "Columbus",
        "state": "OH",
        "zip": "43210",
        "country": "USA"
    }
)
<<<<<<< HEAD
=======

# ❌ 测试 4：无效的折扣码
test_transaction_verification(
    order_id="ORD-Alice-4",
    user_id="user999",
    amount=50,
    credit_card=transaction_verification.CreditCard(
        number="4111111111111111",
        expiration_date="12/25",
        cvv="789"
    ),
    discount_code="INVALIDCODE",
    billing_address={
        "street": "101 Pine St",
        "city": "New York",
        "state": "NY",
        "zip": "10001",
        "country": "USA"
    }
)
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
