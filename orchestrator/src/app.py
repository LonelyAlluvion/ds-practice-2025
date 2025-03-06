import sys
import os
import json
import threading
import grpc
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor
import time

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

# === Flask app setup ===
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

# === gRPC Service Call Functions ===
results_lock = threading.Lock()  # 防止多线程同时修改 results
results = {}

def call_fraud_detection(user_id, amount, billing_address):
    """
    Calls the Fraud Detection Service using gRPC.
    """
    try:
        with grpc.insecure_channel('ds-fraud_detection-1:50051') as channel:
            stub = fraud_detection_grpc.FraudDetectionStub(channel)
            response = stub.CheckFraud(fraud_detection.FraudRequest(
                user_id=user_id,
                amount=amount,
                billing_address=fraud_detection.BillingAddress(
                    street=billing_address.get("street", ""),
                    city=billing_address.get("city", ""),
                    state=billing_address.get("state", ""),
                    zip=billing_address.get("zip", ""),
                    country=billing_address.get("country", ""),
                ),
                timestamp=int(time.time())
            ))

            with results_lock:
                results["fraud"] = response.flagged
            logger.info(f"Fraud Detection Response: {response.flagged}")
    except grpc.RpcError as e:
        with results_lock:
            results["fraud"] = True  # 失败时默认欺诈
        logger.error(f"Fraud Detection Service Error: {e}")

def call_transaction_verification(order_id, amount, credit_card, discount_code, billing_address):
    """
    Calls the Transaction Verification Service using gRPC.
    """
    try:
        with grpc.insecure_channel('ds-transaction_verification-1:50052') as channel:
            stub = transaction_verification_grpc.TransactionVerificationStub(channel)
            response = stub.VerifyTransaction(transaction_verification.TransactionRequest(
                order_id=order_id,
                user_id="dummy_user",  # 这里可以传真实的 user_id
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
            ))

            with results_lock:
                results["transaction"] = response.approved
            logger.info(f"Transaction Verification Response: {response.approved}")
    except grpc.RpcError as e:
        with results_lock:
            results["transaction"] = False  # 失败时默认支付失败
        logger.error(f"Transaction Verification Service Error: {e}")

# def call_suggestions(user_id, purchased_books):
#     """
#     Calls the Suggestions Service using gRPC.
#     """
#     try:
#         with grpc.insecure_channel('ds-suggestions-1:50053') as channel:
#             stub = suggestions_grpc.SuggestionsStub(channel)
#             response = stub.RecommendBooks(suggestions.RecommendationRequest(
#                 order_id="dummy_order",
#                 user_id=user_id,
#                 purchased_books=[
#                     suggestions.Book(book_id=book["bookId"], title=book["title"], author=book["author"])
#                     for book in purchased_books
#                 ]
#             ))
#
#             with results_lock:
#                 results["recommendations"] = [
#                     {"bookId": book.book_id, "title": book.title, "author": book.author}
#                     for book in response.suggested_books
#                 ]
#             logger.info(f"Suggestions Response: {results['recommendations']}")
#     except grpc.RpcError as e:
#         with results_lock:
#             results["recommendations"] = []  # 失败时无推荐
#         logger.error(f"Suggestions Service Error: {e}")

# 新加的，在没有书籍ID也能抛出错误
def call_suggestions(user_id, purchased_books):
    try:
        with grpc.insecure_channel('ds-suggestions-1:50053') as channel:
            stub = suggestions_grpc.SuggestionsStub(channel)
            response = stub.RecommendBooks(suggestions.RecommendationRequest(
                order_id="dummy_order",
                user_id=user_id,
                purchased_books=[
                    suggestions.Book(
                        book_id=book.get("bookId", "unknown"),
                        title=book.get("name", "Unknown Title"),  # ✅ 这里修正
                        author=book.get("author", "Unknown")
                    )
                    for book in purchased_books
                ]
            ))

            with results_lock:
                results["recommendations"] = [
                    {"bookId": book.book_id, "title": book.title, "author": book.author}
                    for book in response.suggested_books
                ]
            logger.info(f"Suggestions Response: {results['recommendations']}")
    except grpc.RpcError as e:
        with results_lock:
            results["recommendations"] = []  # 失败时无推荐
        logger.error(f"Suggestions Service Error: {e}")


# === REST API Endpoints ===
@app.route("/", methods=["GET"])
def index():
    return "Orchestrator Service Running"


@app.route("/checkout", methods=["POST"])
def checkout():
    """
    Handles the checkout process by calling backend microservices.
    """
    # 检查请求头是否是 JSON
    if request.content_type != "application/json":
        logger.warning("Unsupported Media Type: Content-Type must be application/json")
        return jsonify(
            {"error": {"code": "415", "message": "Unsupported Media Type: Content-Type must be application/json"}}), 415

    try:
        request_data = request.get_json()

        # 如果解析 JSON 失败
        if request_data is None:
            logger.warning("Invalid JSON format in request")
            return jsonify({"error": {"code": "400", "message": "Invalid JSON data"}}), 400

        # 打印订单开始分隔线
        logger.info("\n" + "=" * 50)
        logger.info("Processing new order request")

        # 必填字段检查
        required_fields = ["user", "creditCard", "items", "shippingMethod", "termsAccepted"]
        if not all(field in request_data for field in required_fields):
            logger.warning("Missing required fields in request data")
            return jsonify({"error": {"code": "400", "message": "Missing required fields"}}), 400

        if not request_data["termsAccepted"]:
            logger.warning("Terms and Conditions must be accepted")
            return jsonify({"error": {"code": "400", "message": "Terms and Conditions must be accepted"}}), 400

        user_id = request_data["user"]["name"]
        amount = sum(item["quantity"] for item in request_data["items"])
        credit_card = request_data["creditCard"]
        discount_code = request_data.get("discountCode", "")

        billing_address = request_data.get("billingAddress", {})
        user_comment = request_data.get("userComment", "")
        gift_wrapping = request_data.get("giftWrapping", False)
        shipping_method = request_data["shippingMethod"]

        purchased_books = request_data["items"]

        # 多线程并行调用微服务
        threads = [
            threading.Thread(target=call_fraud_detection, args=(user_id, amount, billing_address)),
            threading.Thread(target=call_transaction_verification,
                             args=(f"ORD-{user_id}-{amount}", amount, credit_card, discount_code, billing_address)),
            threading.Thread(target=call_suggestions, args=(user_id, purchased_books))
        ]

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        # 结果整合
        fraud_flagged = results.get("fraud", True)  # 默认欺诈
        transaction_approved = results.get("transaction", False)  # 默认支付失败

        if fraud_flagged or not transaction_approved:
            logger.warning(
                f"Order rejected. Fraud check: {fraud_flagged}, Transaction approved: {transaction_approved}")
            logger.info("=" * 50)
            return jsonify({
                "orderId": "00000",
                "status": "Order Rejected",
                "billingAddress": billing_address,
                "userComment": user_comment,
                "giftWrapping": gift_wrapping,
                "shippingMethod": shipping_method,
                "suggestedBooks": []
            }), 400

        # 订单批准
        logger.info(f"Order approved for user {user_id}")
        logger.info("=" * 50)
        return jsonify({
            "orderId": f"ORD-{user_id}-{amount}",
            "status": "Order Approved",
            "billingAddress": billing_address,
            "userComment": user_comment,
            "giftWrapping": gift_wrapping,
            "shippingMethod": shipping_method,
            "suggestedBooks": results.get("recommendations", [])
        }), 200

    except Exception as e:
        logger.error(f"Exception during checkout: {str(e)}", exc_info=True)
        return jsonify({"error": {"code": "500", "message": str(e)}}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
