import time
import sys
import os
import grpc
from concurrent import futures

# === Import gRPC stubs ===
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
fraud_detection_grpc_path = os.path.abspath(os.path.join(FILE, '../../utils/pb/fraud_detection'))
sys.path.insert(0, fraud_detection_grpc_path)

import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc


def test_fraud_check(order_id, user_id, amount, shipping_method, user_comment, gift_wrapping, billing_address):
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = fraud_detection_pb2_grpc.FraudDetectionStub(channel)

<<<<<<< HEAD
        # Construct the request object
=======
        # 构造请求对象
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
        request = fraud_detection.FraudRequest(
            order_id=order_id,
            user_id=user_id,
            amount=amount,
            shipping_method=shipping_method,
            user_comment=user_comment,
            gift_wrapping=gift_wrapping,
            country=billing_address.country,
            billing_address=fraud_detection.BillingAddress(
                street=billing_address.street,
                city=billing_address.city,
                state=billing_address.state,
                zip=billing_address.zip,
                country=billing_address.country,
            ),
<<<<<<< HEAD
            timestamp=int(time.time())  # Use the current timestamp
        )

        # Send the request and get the response
        response = stub.CheckFraud(request)

        # Print the returned result
        print(f"Fraud Check for Order {order_id}: {response.details.status}, Reason: {response.reason}")


# ✅ Test 1: Normal transaction
=======
            timestamp=int(time.time())  # 使用当前时间戳
        )

        # 发送请求并获取响应
        response = stub.CheckFraud(request)

        # 打印返回的结果
        print(f"Fraud Check for Order {order_id}: {response.details.status}, Reason: {response.reason}")


# ✅ 测试 1：正常交易
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
test_fraud_check(
    "ORD-JohnDoe-3",
    "user567",
    500,
    "Express",
    "Please handle with care.",
    True,
    fraud_detection.BillingAddress(
        street="123 Main St",
        city="Springfield",
        state="IL",
        zip="62701",
        country="USA"
    )
)

<<<<<<< HEAD
# ❌ Test 2: Amount exceeds transaction limit
=======
# ❌ 测试 2：金额超过交易限额
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
test_fraud_check(
    "ORD-AmountExceed-1",
    "user890",
    15000,
    "Express",
    "Please deliver quickly.",
    False,
    fraud_detection.BillingAddress(
        street="456 Oak St",
        city="Chicago",
        state="IL",
        zip="60601",
        country="USA"
    )
)

<<<<<<< HEAD
# ❌ Test 3: Blacklisted user
test_fraud_check(
    "ORD-BlacklistedUser-1",
    "user123",  # user123 is on the blacklist
=======
# ❌ 测试 3：黑名单用户
test_fraud_check(
    "ORD-BlacklistedUser-1",
    "user123",  # user123 是黑名单中的用户
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
    100,
    "Standard",
    "No special request.",
    False,
    fraud_detection.BillingAddress(
        street="789 Elm St",
        city="Columbus",
        state="OH",
        zip="43210",
        country="USA"
    )
)

<<<<<<< HEAD
# ❌ Test 4: High-risk country
=======
# ❌ 测试 4：高风险国家
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
test_fraud_check(
    "ORD-HighRisk-1",
    "user789",
    500,
    "Express",
    "No special request.",
    False,
    fraud_detection.BillingAddress(
        street="12 Unknown St",
        city="Bangkok",
        state="Bangkok",
        zip="10000",
        country="Thailand"
    )
)

<<<<<<< HEAD
# ❌ Test 5: Multiple transactions in a short time
=======
# ❌ 测试 5：短时间内多次交易
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
test_fraud_check(
    "ORD-TooManyOrders-1",
    "user567",
    200,
    "Express",
    "Handle with care",
    True,
    fraud_detection.BillingAddress(
        street="123 Main St",
        city="Springfield",
        state="IL",
        zip="62701",
        country="USA"
    )
)
