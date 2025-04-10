import requests
import json

<<<<<<< HEAD
# Set the target server address
base_url = "http://localhost:8081/checkout"  # Changed to 8081
# Test 1: Successful checkout process
=======
# 设置目标服务器的地址
base_url = "http://localhost:8081/checkout"  # 改为 8081
# 测试 1: 成功的结账流程
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
success_order = {
    "user": {
        "name": "user12388"
    },
    "creditCard": {
        "number": "4111111111111111",
        "expirationDate": "12/25",
        "cvv": "123"
    },
    "items": [
        {"bookId": "123", "title": "How to make money", "author": "John Doe", "quantity": 1},
        {"bookId": "456", "title": "Advanced Math", "author": "Jane Doe", "quantity": 2}
    ],
    "shippingMethod": "Standard",
    "termsAccepted": True,
    "billingAddress": {
        "street": "123 Main St",
        "city": "Springfield",
        "state": "IL",
        "zip": "62701",
        "country": "USA"
    }
}

response = requests.post(base_url, json=success_order)
print(f"Test 1 (Successful Order): {response.json()}")

<<<<<<< HEAD
# Test 2: Missing required fields
=======
# 测试 2: 缺少必填字段
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
missing_field_order = {
    "user": {
        "name": "user123"
    },
    "creditCard": {
        "number": "4111111111111111",
        "expirationDate": "12/25",
        "cvv": "123"
    },
    "shippingMethod": "Standard",
    "termsAccepted": True
<<<<<<< HEAD
    # Missing 'items' field
=======
    # 缺少 items 字段
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
}

response = requests.post(base_url, json=missing_field_order)
print(f"Test 2 (Missing Fields): {response.json()}")

<<<<<<< HEAD
# Test 3: Payment verification failed (simulate failure)
=======
# 测试 3: 支付验证失败 (模拟失败)
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
payment_failure_order = {
    "user": {
        "name": "user1231"
    },
    "creditCard": {
        "number": "4111111111111111",
        "expirationDate": "12/25",
<<<<<<< HEAD
        "cvv": "999" # use a invalid cvv
=======
        "cvv": "123"
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
    },
    "items": [
        {"bookId": "123", "title": "Human history", "author": "John Doe", "quantity": 1}
    ],
    "shippingMethod": "Standard",
    "termsAccepted": True,
    "billingAddress": {
        "street": "123 Main St",
        "city": "Springfield",
        "state": "IL",
        "zip": "62701",
        "country": "USA"
    }
}

response = requests.post(base_url, json=payment_failure_order)
print(f"Test 3 (Payment Verification Failed): {response.json()}")

<<<<<<< HEAD
# Test 4: Fraud detection failed (simulate failure)
=======
# 测试 4: 欺诈检测失败 (模拟失败)
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
fraud_failure_order = {
    "user": {
        "name": "user123"
    },
    "creditCard": {
        "number": "4111111111111111",
        "expirationDate": "12/25",
        "cvv": "123"
    },
    "items": [
        {"bookId": "123", "title": "How to cook well", "author": "John Doe", "quantity": 1}
    ],
    "shippingMethod": "Standard",
    "termsAccepted": True,
    "billingAddress": {
        "street": "123 Main St",
        "city": "Springfield",
        "state": "IL",
        "zip": "62701",
        "country": "USA"
    }
}

response = requests.post(base_url, json=fraud_failure_order)
print(f"Test 4 (Fraud Detection Failed): {response.json()}")
<<<<<<< HEAD
=======

# 测试 5: 推荐书籍
recommendation_test_order = {
    "user": {
        "name": "user123"
    },
    "creditCard": {
        "number": "4111111111111111",
        "expirationDate": "12/25",
        "cvv": "123"
    },
    "items": [
        {"bookId": "123", "title": "Europe Culture", "author": "John Doe", "quantity": 1}
    ],
    "shippingMethod": "Standard",
    "termsAccepted": True,
    "billingAddress": {
        "street": "123 Main St",
        "city": "Springfield",
        "state": "IL",
        "zip": "62701",
        "country": "USA"
    }
}

response = requests.post(base_url, json=recommendation_test_order)
print(f"Test 5 (Book Recommendations): {response.json()}")

# 测试 6: 服务不可用（模拟故障）
service_failure_order = {
    "user": {
        "name": "user123"
    },
    "creditCard": {
        "number": "4111111111111111",
        "expirationDate": "12/25",
        "cvv": "123"
    },
    "items": [
        {"bookId": "123", "title": "Math", "author": "John Doe", "quantity": 1}
    ],
    "shippingMethod": "Standard",
    "termsAccepted": True,
    "billingAddress": {
        "street": "123 Main St",
        "city": "Springfield",
        "state": "IL",
        "zip": "62701",
        "country": "USA"
    }
}

response = requests.post(base_url, json=service_failure_order)
print(f"Test 6 (Service Unavailable): {response.json()}")


>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
