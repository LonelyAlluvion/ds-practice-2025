import requests
import json

# Set the target server address
base_url = "http://localhost:8081/checkout"  # Changed to 8081
# Test 1: Successful checkout process
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

# Test 2: Missing required fields
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
    # Missing 'items' field
}

response = requests.post(base_url, json=missing_field_order)
print(f"Test 2 (Missing Fields): {response.json()}")

# Test 3: Payment verification failed (simulate failure)
payment_failure_order = {
    "user": {
        "name": "user1231"
    },
    "creditCard": {
        "number": "4111111111111111",
        "expirationDate": "12/25",
        "cvv": "999" # use a invalid cvv
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

# Test 4: Fraud detection failed (simulate failure)
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
