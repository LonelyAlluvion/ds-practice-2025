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

<<<<<<< HEAD
# === 配置支付验证规则 ===
VALID_DISCOUNT_CODES = {"SAVE10": 0.1, "VIP20": 0.2}  # 10% 和 20% 折扣
VALID_CVV = {"123", "456", "789"}  # 假设这些 CVV 号有效
CREDIT_CARD_EXPIRATION_FORMAT = "%m/%y"  # MM/YY 格式
=======
# === Payment verification rules ===
VALID_DISCOUNT_CODES = {"SAVE10": 0.1, "VIP20": 0.2}  # 10% and 20% discount
VALID_CVV = {"123", "456", "789"}  # Example valid CVVs
CREDIT_CARD_EXPIRATION_FORMAT = "%m/%y"  # MM/YY format

# Store order data and vector clocks
order_cache = {}

>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)

class TransactionVerificationService(transaction_verification_pb2_grpc.TransactionVerificationServicer):
    def VerifyTransaction(self, request, context):
        """
<<<<<<< HEAD
        - 检查信用卡是否过期
        - 验证 CVV
        - 验证折扣码
        - 计算最终支付金额
=======
        - Check if the credit card has expired.
        - Validate CVV.
        - Validate discount code.
        - Calculate the final charged amount.
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
        """
        user_id = request.user_id
        order_id = request.order_id
        amount = request.amount
        credit_card = request.credit_card
        discount_code = request.discount_code
        billing_address = request.billing_address
<<<<<<< HEAD

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
=======
        vector_clock = list(request.vector_clock)

        logger.info(f"[Transaction Verification] --- Start: Processing Order {order_id} ---")
        logger.debug(f"[Transaction Verification] gRPC Request: {request}")

        # Store order data in cache
        order_cache[order_id] = {
            "user_id": user_id,
            "amount": amount,
            "vector_clock": vector_clock,
        }

        # 1️⃣ Check if the credit card is expired
        if not self._validate_expiration_date(credit_card.expiration_date):
            logger.warning(f"[Transaction Verification] ❌ Order {order_id} rejected: Credit card expired")
            return self._reject(order_id, "Credit card expired", billing_address, discount_code, amount, vector_clock)

        # 2️⃣ Validate CVV
        if credit_card.cvv not in VALID_CVV:
            logger.warning(f"[Transaction Verification] ❌ Order {order_id} rejected: Invalid CVV")
            return self._reject(order_id, "Invalid CVV", billing_address, discount_code, amount, vector_clock)

        # 3️⃣ Calculate final charged amount after discount
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
        charged_amount = amount
        if discount_code in VALID_DISCOUNT_CODES:
            discount = VALID_DISCOUNT_CODES[discount_code]
            charged_amount = round(amount * (1 - discount), 2)
        else:
<<<<<<< HEAD
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
=======
            discount_code = "None"  # No discount applied

        vector_clock[0] += 1
        logger.info(f"[Transaction Verification] ✅ Order {order_id} approved, Final Amount: {charged_amount}")
        logger.info(f"[Transaction Verification] Updated Vector Clock: {vector_clock}")
        logger.info(f"[Transaction Verification] --- End: Processing Order {order_id} ---")

        return transaction_verification.TransactionResponse(
            approved=True,
            reason="Payment approved",
            details=self._build_details(order_id, "Payment Successful", billing_address, discount_code, charged_amount),
            vector_clock=vector_clock
        )

    def _validate_expiration_date(self, expiration_date):
        """Check if the credit card has expired."""
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
        try:
            exp_date = datetime.strptime(expiration_date, CREDIT_CARD_EXPIRATION_FORMAT)
            return exp_date > datetime.now()
        except ValueError:
            return False

<<<<<<< HEAD
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
=======
    def _reject(self, order_id, reason, billing_address, discount_code, amount, vector_clock):
        """Return response for rejected payment."""
        logger.error(f"[Transaction Verification] ❌ Rejecting Order {order_id}: {reason}")
        vector_clock[0] += 1
        logger.info(f"[Transaction Verification] Updated Vector Clock: {vector_clock}")
        logger.info(f"[Transaction Verification] --- End: Processing Order {order_id} ---")

        return transaction_verification.TransactionResponse(
            approved=False,
            reason=reason,
            details=self._build_details(order_id, "Payment Rejected", billing_address, discount_code, amount),
            vector_clock=vector_clock
        )

    def _build_details(self, order_id, status, billing_address, discount_code, charged_amount):
        """Generate transaction details."""
        logger.debug(f"[Transaction Verification] 📑 Building details for Order ID: {order_id} with status {status}")
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
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

<<<<<<< HEAD
def serve():
    """
    启动 gRPC 服务器，监听 50052 端口
=======
    def ClearOrderData(self, request, context):
        """Clear stored order data only if local vector clock <= final vector clock."""
        order_id = request.order_id
        vc_final = list(request.vector_clock)

        def is_vc_less_equal(vc1, vc2):
            return all(x <= y for x, y in zip(vc1, vc2))

        if order_id in order_cache:
            vc_local = order_cache[order_id]["vector_clock"]
            if is_vc_less_equal(vc_local, vc_final):
                del order_cache[order_id]
                logger.info(f"[Transaction Verification] 🗑 Cleared order data for Order ID: {order_id}")
                return transaction_verification.ClearOrderResponse(success=True)
            else:
                logger.warning(f"[Transaction Verification] ⚠️ Rejecting cleanup for Order ID: {order_id} - Local VC {vc_local} is newer than Final VC {vc_final}")
                return transaction_verification.ClearOrderResponse(success=False)

        return transaction_verification.ClearOrderResponse(success=False)



def serve():
    """
    Start gRPC server, listening on port 50052.
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    transaction_verification_pb2_grpc.add_TransactionVerificationServicer_to_server(TransactionVerificationService(), server)

    port = "50052"
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logger.info(f"[Transaction Verification Service] 🚀 Running on port {port}...")
    server.wait_for_termination()

<<<<<<< HEAD
=======

>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
if __name__ == "__main__":
    serve()
