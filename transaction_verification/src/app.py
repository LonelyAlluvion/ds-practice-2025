import sys
import os
import grpc
import time
from datetime import datetime
import logging
from concurrent import futures

# === Configure logging ===
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# === Import gRPC stubs ===
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
transaction_verification_grpc_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/transaction_verification'))
sys.path.insert(0, transaction_verification_grpc_path)

import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc

# === 配置支付验证规则 ===
VALID_DISCOUNT_CODES = {"SAVE10": 0.1, "VIP20": 0.2}  # 10% 和 20% 折扣
VALID_CVV = {"123", "456", "789"}  # 假设这些 CVV 号有效
CREDIT_CARD_EXPIRATION_FORMAT = "%m/%y"  # MM/YY 格式

class TransactionVerificationService(transaction_verification_pb2_grpc.TransactionVerificationServicer):
    def VerifyTransaction(self, request, context):
        """
        - 检查信用卡是否过期
        - 验证 CVV
        - 验证折扣码
        - 计算最终支付金额
        """
        user_id = request.user_id
        order_id = request.order_id
        amount = request.amount
        credit_card = request.credit_card
        discount_code = request.discount_code
        billing_address = request.billing_address

        # 输出开始的分隔线
        logger.info("\n" + "="*40)
        logger.info(f"[Transaction Verification] Checking Order ID: {order_id}, User ID: {user_id}, Amount: {amount}")

        # 1️⃣ 检查信用卡是否过期
        if not self._validate_expiration_date(credit_card.expiration_date):
            logger.warning(f"[Transaction Verification] ❌ Order {order_id} rejected: Credit card expired")
            return self._reject(order_id, "Credit card expired", billing_address, discount_code, amount)

        # 2️⃣ 检查 CVV 是否有效
        if credit_card.cvv not in VALID_CVV:
            logger.warning(f"[Transaction Verification] ❌ Order {order_id} rejected: Invalid CVV")
            return self._reject(order_id, "Invalid CVV", billing_address, discount_code, amount)

        # 3️⃣ 计算折扣后的金额
        charged_amount = amount
        if discount_code in VALID_DISCOUNT_CODES:
            discount = VALID_DISCOUNT_CODES[discount_code]
            charged_amount = round(amount * (1 - discount), 2)
        else:
            discount_code = "None"  # 没有使用折扣码

        logger.info(f"[Transaction Verification] ✅ Order {order_id} Approved, Final Amount: {charged_amount}")

        # 输出结束的分隔线
        logger.info("="*40)

        # 订单通过验证
        return transaction_verification.TransactionResponse(
            approved=True,
            reason="Payment approved",
            details=self._build_details(order_id, "Payment Successful", billing_address, discount_code, charged_amount)
        )

    def _validate_expiration_date(self, expiration_date):
        """ 检查信用卡是否过期 """
        try:
            exp_date = datetime.strptime(expiration_date, CREDIT_CARD_EXPIRATION_FORMAT)
            return exp_date > datetime.now()
        except ValueError:
            return False

    def _reject(self, order_id, reason, billing_address, discount_code, amount):
        """ 返回支付拒绝信息 """
        logger.error(f"[Transaction Verification] ❌ Rejecting Order {order_id}: {reason}")
        return transaction_verification.TransactionResponse(
            approved=False,
            reason=reason,
            details=self._build_details(order_id, "Payment Rejected", billing_address, discount_code, amount)
        )

    def _build_details(self, order_id, status, billing_address, discount_code, charged_amount):
        """ 生成交易详情 """
        logger.debug(f"[Transaction Verification] Building details for Order ID: {order_id} with status {status}")
        return transaction_verification.TransactionDetails(
            order_id=order_id,
            status=status,
            billing_address=transaction_verification.BillingAddress(
                street=billing_address.street,
                city=billing_address.city,
                state=billing_address.state,
                zip=billing_address.zip,
                country=billing_address.country,
            ),
            discount_code=discount_code,
            charged_amount=charged_amount
        )

def serve():
    """
    启动 gRPC 服务器，监听 50052 端口
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    transaction_verification_pb2_grpc.add_TransactionVerificationServicer_to_server(TransactionVerificationService(), server)

    port = "50052"
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logger.info(f"[Transaction Verification Service] 🚀 Running on port {port}...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
