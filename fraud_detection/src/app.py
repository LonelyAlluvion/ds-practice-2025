import sys
import os
import grpc
import time
import logging
from concurrent import futures

# === Configure logging ===
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# === Import gRPC stubs ===
FILE = os.path.abspath(__file__) if '__file__' in globals() else os.getcwd()
fraud_detection_grpc_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(0, fraud_detection_grpc_path)

import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc

<<<<<<< HEAD
# === 配置欺诈检测规则 ===
TRANSACTION_LIMIT = 10000  # 超过 10000 视为欺诈
BLACKLISTED_USERS = {"user123", "user999"}  # 黑名单用户
HIGH_RISK_COUNTRIES = {"Myanmar", "Thailand"}  # 高风险国家

# 订单记录（用于短时间多次交易检测），格式：{user_id: [timestamp1, timestamp2, ...]}
user_transactions = {}
=======
# === Fraud detection rules ===
TRANSACTION_LIMIT = 10000  # Transactions above this amount are flagged as fraudulent
BLACKLISTED_USERS = {"user123", "user999"}  # Blacklisted users
HIGH_RISK_COUNTRIES = {"Myanmar", "Thailand"}  # High-risk countries

# Order history for detecting frequent transactions within a short time
user_transactions = {}
# Store order data and vector clocks
order_cache = {}
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)


class FraudDetectionService(fraud_detection_pb2_grpc.FraudDetectionServicer):
    def CheckFraud(self, request, context):
        """
<<<<<<< HEAD
        - 检查交易金额是否超过 10000
        - 检查用户是否在黑名单中
        - 检查用户是否来自高风险地区
        - 检查用户是否在 1 小时内下单超过 5 次
=======
        Fraud detection checks:
        - If transaction amount exceeds 10000
        - If user is blacklisted
        - If user is from a high-risk country
        - If user has placed more than 5 orders within 1 hour
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
        """
        user_id = request.user_id
        order_id = request.order_id
        amount = request.amount
        shipping_method = request.shipping_method
        user_comment = request.user_comment
        gift_wrapping = request.gift_wrapping
<<<<<<< HEAD
        country = request.country
        billing_address = request.billing_address
        timestamp = request.timestamp

        # 在每个订单处理开始时打印分隔符
        logger.info("\n" + "=" * 40)  # 打印一条横线分隔符
        logger.info(f"[Fraud Detection] Checking fraud for Order ID: {order_id}, User ID: {user_id}, Amount: {amount}")

        # 1️⃣ 交易金额检测
        if amount > TRANSACTION_LIMIT:
            logger.warning(f"[Fraud Detection] 🚨 Order {order_id} flagged: Amount exceeds limit")
            return self._reject(order_id, "Transaction amount exceeds limit", billing_address, user_comment,
                                gift_wrapping, shipping_method)

        # 2️⃣ 用户黑名单检测
        if user_id in BLACKLISTED_USERS:
            logger.warning(f"[Fraud Detection] 🚨 Order {order_id} flagged: User is blacklisted")
            return self._reject(order_id, "User is blacklisted", billing_address, user_comment, gift_wrapping,
                                shipping_method)

        # 3️⃣ 高风险地区检测
        if country in HIGH_RISK_COUNTRIES:
            logger.warning(f"[Fraud Detection] 🚨 Order {order_id} flagged: User from high-risk country: {country}")
            return self._reject(order_id, f"User from high-risk country: {country}", billing_address, user_comment,
                                gift_wrapping, shipping_method)

        # 4️⃣ 短时间多次交易检测
        now = int(time.time())
        if user_id not in user_transactions:
            user_transactions[user_id] = []

        # 移除超过 1 小时的订单记录
=======
        country = request.billing_address.country
        billing_address = request.billing_address
        timestamp = request.timestamp
        vector_clock = list(request.vector_clock)

        logger.info(f"[Fraud Detection] --- Start: Processing Order {order_id} ---")
        logger.debug(f"[Fraud Detection] gRPC Request: {request}")

        # Store order data
        order_cache[order_id] = {
            "user_id": user_id,
            "amount": amount,
            "vector_clock": vector_clock,
        }

        # 1️⃣ Transaction amount check
        if amount > TRANSACTION_LIMIT:
            logger.warning(f"[Fraud Detection] 🚨 Order {order_id} flagged: Transaction amount exceeds limit")
            return self._reject(order_id, "Transaction amount exceeds limit", billing_address, user_comment,
                                gift_wrapping, shipping_method, vector_clock)

        # 2️⃣ Blacklisted user check
        if user_id in BLACKLISTED_USERS:
            logger.warning(f"[Fraud Detection] 🚨 Order {order_id} flagged: User is blacklisted")
            return self._reject(order_id, "User is blacklisted", billing_address, user_comment, gift_wrapping,
                                shipping_method, vector_clock)

        # 3️⃣ High-risk country check
        if country in HIGH_RISK_COUNTRIES:
            logger.warning(f"[Fraud Detection] 🚨 Order {order_id} flagged: User from high-risk country: {country}")
            return self._reject(order_id, f"User from high-risk country: {country}", billing_address, user_comment,
                                gift_wrapping, shipping_method, vector_clock)

        # 4️⃣ Frequent transaction detection
        now = int(time.time())
        if user_id not in user_transactions:
            user_transactions[user_id] = []
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
        user_transactions[user_id] = [t for t in user_transactions[user_id] if now - t <= 3600]
        user_transactions[user_id].append(timestamp)

        if len(user_transactions[user_id]) > 5:
            logger.warning(f"[Fraud Detection] 🚨 Order {order_id} flagged: Too many transactions in a short period")
            return self._reject(order_id, "Too many transactions in a short period", billing_address, user_comment,
<<<<<<< HEAD
                                gift_wrapping, shipping_method)

        # 订单安全
        logger.info(f"[Fraud Detection] ✅ Order {order_id} is safe")
=======
                                gift_wrapping, shipping_method, vector_clock)

        # Update vector clock
        vector_clock[1] += 1
        logger.info(f"[Fraud Detection] ✅ Order {order_id} is safe")
        logger.info(f"[Fraud Detection] Updated Vector Clock: {vector_clock}")
        logger.info(f"[Fraud Detection] --- End: Processing Order {order_id} ---")

>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
        return fraud_detection.FraudResponse(
            flagged=False,
            reason="Transaction is safe",
            details=self._build_details(order_id, "Order Approved", billing_address, user_comment, gift_wrapping,
<<<<<<< HEAD
                                        shipping_method)
        )

    def _reject(self, order_id, reason, billing_address, user_comment, gift_wrapping, shipping_method):
=======
                                        shipping_method),
            vector_clock=vector_clock
        )

    def _reject(self, order_id, reason, billing_address, user_comment, gift_wrapping, shipping_method, vector_clock):
        """
        Returns response when an order is rejected.
        """
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
        logger.error(f"[Fraud Detection] ❌ Rejecting Order {order_id}: {reason}")
        return fraud_detection.FraudResponse(
            flagged=True,
            reason=reason,
            details=self._build_details(order_id, "Order Rejected", billing_address, user_comment, gift_wrapping,
<<<<<<< HEAD
                                        shipping_method)
        )

    def _build_details(self, order_id, status, billing_address, user_comment, gift_wrapping, shipping_method):
        logger.debug(f"[Fraud Detection] Building details for Order ID: {order_id} with status {status}")
=======
                                        shipping_method),
            vector_clock=vector_clock
        )

    def _build_details(self, order_id, status, billing_address, user_comment, gift_wrapping, shipping_method):
        """
        Builds FraudCheckDetails response structure.
        """
        logger.debug(f"[Fraud Detection] 🛠️ Building details for Order ID: {order_id} with status {status}")
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
        return fraud_detection.FraudCheckDetails(
            order_id=order_id,
            status=status,
            billing_address=fraud_detection.BillingAddress(
                street=billing_address.street,
                city=billing_address.city,
                state=billing_address.state,
                zip=billing_address.zip,
                country=billing_address.country,
            ),
            user_comment=user_comment,
            gift_wrapping=gift_wrapping,
            shipping_method=shipping_method
        )

<<<<<<< HEAD

def serve():
    """
    启动 gRPC 服务器，监听 50051 端口
=======
    def ClearOrderData(self, request, context):
        """
        Clears stored order data only if local vector clock <= final vector clock.
        """
        order_id = request.order_id
        vc_final = list(request.vector_clock)

        def is_vc_less_equal(vc1, vc2):
            return all(x <= y for x, y in zip(vc1, vc2))

        if order_id in order_cache:
            vc_local = order_cache[order_id]["vector_clock"]
            if is_vc_less_equal(vc_local, vc_final):
                del order_cache[order_id]
                logger.info(f"[Fraud Detection] 🗑️ Cleared order data for Order ID: {order_id}")
                return fraud_detection.ClearOrderResponse(success=True)
            else:
                logger.warning(f"[Fraud Detection] ⚠️ Rejecting cleanup for Order ID: {order_id} - Local VC {vc_local} is newer than Final VC {vc_final}")
                return fraud_detection.ClearOrderResponse(success=False)

        return fraud_detection.ClearOrderResponse(success=False)


def serve():
    """
    Starts gRPC server, listening on port 50051.
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    fraud_detection_pb2_grpc.add_FraudDetectionServicer_to_server(FraudDetectionService(), server)

    port = "50051"
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logger.info(f"[Fraud Detection Service] 🚀 Running on port {port}...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
