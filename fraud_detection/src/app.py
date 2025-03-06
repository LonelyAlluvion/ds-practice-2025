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

# === 配置欺诈检测规则 ===
TRANSACTION_LIMIT = 10000  # 超过 10000 视为欺诈
BLACKLISTED_USERS = {"user123", "user999"}  # 黑名单用户
HIGH_RISK_COUNTRIES = {"Myanmar", "Thailand"}  # 高风险国家

# 订单记录（用于短时间多次交易检测），格式：{user_id: [timestamp1, timestamp2, ...]}
user_transactions = {}


class FraudDetectionService(fraud_detection_pb2_grpc.FraudDetectionServicer):
    def CheckFraud(self, request, context):
        """
        - 检查交易金额是否超过 10000
        - 检查用户是否在黑名单中
        - 检查用户是否来自高风险地区
        - 检查用户是否在 1 小时内下单超过 5 次
        """
        user_id = request.user_id
        order_id = request.order_id
        amount = request.amount
        shipping_method = request.shipping_method
        user_comment = request.user_comment
        gift_wrapping = request.gift_wrapping
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
        user_transactions[user_id] = [t for t in user_transactions[user_id] if now - t <= 3600]
        user_transactions[user_id].append(timestamp)

        if len(user_transactions[user_id]) > 5:
            logger.warning(f"[Fraud Detection] 🚨 Order {order_id} flagged: Too many transactions in a short period")
            return self._reject(order_id, "Too many transactions in a short period", billing_address, user_comment,
                                gift_wrapping, shipping_method)

        # 订单安全
        logger.info(f"[Fraud Detection] ✅ Order {order_id} is safe")
        return fraud_detection.FraudResponse(
            flagged=False,
            reason="Transaction is safe",
            details=self._build_details(order_id, "Order Approved", billing_address, user_comment, gift_wrapping,
                                        shipping_method)
        )

    def _reject(self, order_id, reason, billing_address, user_comment, gift_wrapping, shipping_method):
        logger.error(f"[Fraud Detection] ❌ Rejecting Order {order_id}: {reason}")
        return fraud_detection.FraudResponse(
            flagged=True,
            reason=reason,
            details=self._build_details(order_id, "Order Rejected", billing_address, user_comment, gift_wrapping,
                                        shipping_method)
        )

    def _build_details(self, order_id, status, billing_address, user_comment, gift_wrapping, shipping_method):
        logger.debug(f"[Fraud Detection] Building details for Order ID: {order_id} with status {status}")
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


def serve():
    """
    启动 gRPC 服务器，监听 50051 端口
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
