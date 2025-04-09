import sys
import os
import json
import threading
import grpc
import logging
import time
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor

# === Configure logging ===
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# === Import gRPC stubs ===
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")

# Fraud Detection Service
fraud_detection_grpc_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(0, fraud_detection_grpc_path)
import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc

# Transaction Verification Service
transaction_verification_grpc_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/transaction_verification'))
sys.path.insert(0, transaction_verification_grpc_path)
import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc

# Suggestions Service
suggestions_grpc_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/suggestions'))
sys.path.insert(0, suggestions_grpc_path)
import suggestions_pb2 as suggestions
import suggestions_pb2_grpc as suggestions_grpc

# Order Queue Service
order_queue_grpc_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_queue'))
sys.path.insert(0, order_queue_grpc_path)
import order_queue_pb2 as order_queue
import order_queue_pb2_grpc as order_queue_grpc

# === Flask app setup ===
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

# === gRPC Service Call Functions ===
results_lock = threading.Lock()
results = {}

def generate_order_id():
    return str(uuid.uuid4())

def broadcast_clear_order(order_id, vector_clock):
    logger.info(f"[Orchestrator] \U0001f4e2 Broadcasting order cleanup for Order ID: {order_id}")
    logger.info(f"[Orchestrator] Final Vector Clock for cleanup: {vector_clock}")

    services = [
        ("ds-transaction_verification-1:50052", transaction_verification_grpc.TransactionVerificationStub),
        ("ds-fraud_detection-1:50051", fraud_detection_grpc.FraudDetectionStub),
        ("ds-suggestions-1:50053", suggestions_grpc.SuggestionsStub),
    ]

    for service_addr, stub_class in services:
        try:
            with grpc.insecure_channel(service_addr) as channel:
                stub = stub_class(channel)
                request = transaction_verification.ClearOrderRequest(order_id=order_id, vector_clock=vector_clock)
                response = stub.ClearOrderData(request)
                if response.success:
                    logger.info(f"[Orchestrator] ✅ Cleared order data in {service_addr}")
                else:
                    logger.warning(f"[Orchestrator] ⚠️ Failed to clear order data in {service_addr}")
        except grpc.RpcError as e:
            logger.error(f"[Orchestrator] ❌ Error clearing order data in {service_addr}: {e}")

def enqueue_order_to_queue(order_id, user_id, total_amount):
    try:
        with grpc.insecure_channel("ds-order_queue-1:50054") as channel:
            stub = order_queue_grpc.OrderQueueStub(channel)
            request = order_queue.EnqueueRequest(
                order_id=order_id,
                user_id=user_id,
                amount=total_amount


            )
            response = stub.EnqueueOrder(request)
            if response.success:
                logger.info(f"[Orchestrator] ✅ Order {order_id} enqueued successfully.")
            else:
                logger.warning(f"[Orchestrator] ⚠️ Failed to enqueue order {order_id}.")
    except grpc.RpcError as e:
        logger.error(f"[Orchestrator] ❌ gRPC Error while enqueuing order: {e}")

def call_transaction_verification(order_id, user_id, amount, credit_card, discount_code, billing_address, vector_clock):
    logger.info(f"[Orchestrator] Step 1: Calling Transaction Verification for Order ID: {order_id}")

    try:
        request = transaction_verification.TransactionRequest(
            order_id=order_id,
            user_id=user_id,
            amount=amount,
            credit_card=transaction_verification.CreditCard(
                number=credit_card["number"],
                expiration_date=credit_card["expirationDate"],
                cvv=credit_card["cvv"],
            ),
            discount_code=discount_code,
            billing_address=transaction_verification.BillingAddress(
                street=billing_address.get("street", ""),
                city=billing_address.get("city", ""),
                state=billing_address.get("state", ""),
                zip=billing_address.get("zip", ""),
                country=billing_address.get("country", ""),
            ),
            vector_clock=vector_clock
        )

        with grpc.insecure_channel('ds-transaction_verification-1:50052') as channel:
            stub = transaction_verification_grpc.TransactionVerificationStub(channel)
            response = stub.VerifyTransaction(request)

            with results_lock:
                results["transaction"] = response.approved
                results["vector_clock"] = response.vector_clock

    except grpc.RpcError as e:
        with results_lock:
            results["transaction"] = False
        logger.error(f"[Orchestrator] Transaction Verification Service Error: {e}")

def call_fraud_detection(order_id, user_id, amount, billing_address, vector_clock):
    logger.info(f"[Orchestrator] Step 2: Calling Fraud Detection for Order ID: {order_id}")

    try:
        request = fraud_detection.FraudRequest(
            order_id=order_id,
            user_id=user_id,
            amount=amount,
            billing_address=fraud_detection.BillingAddress(
                street=billing_address.get("street", ""),
                city=billing_address.get("city", ""),
                state=billing_address.get("state", ""),
                zip=billing_address.get("zip", ""),
                country=billing_address.get("country", ""),
            ),
            timestamp=int(time.time()),
            vector_clock=vector_clock
        )

        with grpc.insecure_channel('ds-fraud_detection-1:50051') as channel:
            stub = fraud_detection_grpc.FraudDetectionStub(channel)
            response = stub.CheckFraud(request)

            with results_lock:
                results["fraud"] = response.flagged
                results["vector_clock"] = response.vector_clock

    except grpc.RpcError as e:
        with results_lock:
            results["fraud"] = True
        logger.error(f"[Orchestrator] Fraud Detection Service Error: {e}")

def call_suggestions(order_id, user_id, purchased_books, vector_clock):
    logger.info(f"[Orchestrator] Step 3: Calling Book Recommendations for Order ID: {order_id}")

    try:
        request = suggestions.RecommendationRequest(
            order_id=order_id,
            user_id=user_id,
            purchased_books=[suggestions.Book(book_id=book.get("bookId", "unknown"),
                                              title=book.get("name", "Unknown Title"),
                                              author=book.get("author", "Unknown"))
                             for book in purchased_books],
            vector_clock=vector_clock
        )

        with grpc.insecure_channel('ds-suggestions-1:50053') as channel:
            stub = suggestions_grpc.SuggestionsStub(channel)
            response = stub.RecommendBooks(request)

            with results_lock:
                results["recommendations"] = [
                    {"bookId": book.book_id, "title": book.title, "author": book.author}
                    for book in response.suggested_books
                ]
                results["vector_clock"] = response.vector_clock

    except grpc.RpcError as e:
        with results_lock:
            results["recommendations"] = []
        logger.error(f"[Orchestrator] Suggestions Service Error: {e}")

@app.route("/checkout", methods=["POST"])
def checkout():
    logger.info("\n" + "=" * 50)
    logger.info("[Orchestrator] Processing new order request")

    try:
        request_data = request.get_json()
        order_id = generate_order_id()
        user_id = request_data["user"]["name"]
        amount = sum(item["quantity"] for item in request_data["items"])
        credit_card = request_data["creditCard"]
        discount_code = request_data.get("discountCode", "")
        billing_address = request_data.get("billingAddress", {})
        purchased_books = request_data["items"]
        vector_clock = [0, 0, 0]

        threads = [
            threading.Thread(target=call_transaction_verification, args=(order_id, user_id, amount, credit_card, discount_code, billing_address, vector_clock)),
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        if not results.get("transaction", False):
            broadcast_clear_order(order_id, results["vector_clock"])
            return jsonify({"orderId": "00000", "status": "Order Rejected"}), 400

        call_fraud_detection(order_id, user_id, amount, billing_address, results["vector_clock"])
        if results.get("fraud", True):
            broadcast_clear_order(order_id, results["vector_clock"])
            return jsonify({"orderId": "00000", "status": "Order Rejected"}), 400

        call_suggestions(order_id, user_id, purchased_books, results["vector_clock"])
        enqueue_order_to_queue(order_id, user_id, amount)
        broadcast_clear_order(order_id, results["vector_clock"])

        return jsonify({
            "orderId": order_id,
            "status": "Order Approved",
            "suggestedBooks": results.get("recommendations", [])
        }), 200

    except Exception as e:
        logger.error(f"[Orchestrator] Exception during checkout: {str(e)}", exc_info=True)
        return jsonify({"error": {"code": "500", "message": str(e)}}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
