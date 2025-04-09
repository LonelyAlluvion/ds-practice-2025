import sys
import os
import grpc
import logging
from concurrent import futures

# === Configure logging ===
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# === Import gRPC stubs ===
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
queue_proto_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_queue'))
sys.path.insert(0, queue_proto_path)

import order_queue_pb2 as order_queue
import order_queue_pb2_grpc as order_queue_grpc

# === Internal Order Queue ===
order_queue_list = []

class OrderQueueService(order_queue_grpc.OrderQueueServicer):
    def EnqueueOrder(self, request, context):
        """
        Append a new order to the queue.
        """
        logger.info(f"[Order Queue] ➕ Enqueueing Order ID: {request.order_id}")
        order_queue_list.append(request)
        return order_queue.EnqueueResponse(success=True, message="Order enqueued")

    def DequeueOrder(self, request, context):
        """
        Remove and return the next order from the queue.
        """
        if order_queue_list:
            next_order = order_queue_list.pop(0)
            logger.info(f"[Order Queue] ➖ Dequeuing Order ID: {next_order.order_id}")
            return order_queue.DequeueResponse(
                success=True,
                order=order_queue.Order(
                    order_id=next_order.order_id,
                    user_id=next_order.user_id,
                    amount=next_order.amount,
                    items=next_order.items,
                    billing_address=next_order.billing_address,
                    shipping_method=next_order.shipping_method,
                    user_comment=next_order.user_comment,
                    gift_wrapping=next_order.gift_wrapping
                )
            )
        else:
            logger.info("[Order Queue] 💤 No orders in the queue.")
            return order_queue.DequeueResponse(success=False, order=order_queue.Order())

    def ClearOrderData(self, request, context):
        """
        Optional: Clear an order manually (no-op for now).
        """
        logger.info(f"[Order Queue] 🧹 ClearOrderData called for Order ID: {request.order_id} (noop)")
        return order_queue.ClearOrderResponse(success=True)


def serve():
    """
    Start gRPC server on port 50054.
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_queue_grpc.add_OrderQueueServicer_to_server(OrderQueueService(), server)

    port = "50054"
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logger.info(f"[Order Queue Service] 🚀 Running on port {port}...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
