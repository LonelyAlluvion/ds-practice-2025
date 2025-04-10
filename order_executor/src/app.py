import sys
import os
import grpc
import time
import logging
import threading
from concurrent import futures

# === Configure logging ===
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# === Import gRPC stubs ===
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
order_queue_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_queue'))
sys.path.insert(0, order_queue_path)

import order_queue_pb2 as order_queue
import order_queue_pb2_grpc as order_queue_grpc

# === Import Leader Election Client ===
from election_client import ElectionClient
from election_service import serve as start_election_server  # ✅ 新增导入

# === Configuration ===
ORDER_QUEUE_HOST = os.getenv("ORDER_QUEUE_HOST", "order_queue")
ORDER_QUEUE_PORT = os.getenv("ORDER_QUEUE_PORT", "50054")
POLL_INTERVAL = int(os.getenv("EXECUTOR_POLL_INTERVAL", 5))  # seconds

class OrderExecutor:
    def __init__(self):
        self.channel = grpc.insecure_channel(f"{ORDER_QUEUE_HOST}:{ORDER_QUEUE_PORT}")
        self.stub = order_queue_grpc.OrderQueueStub(self.channel)
        self.election = ElectionClient()  # Initialize ElectionClient to handle leader election
        self.running = True
        self.polling_thread = None

    def process_orders(self):
        """
        Continuously dequeue and process orders from the queue.
        Should run only when this node is the current leader.
        """
        logger.info("[Order Executor] 👑 I am the leader. Starting to process orders.")
        while self.running:
            # Check leader status on each iteration
            if not self.election.is_leader:
                logger.warning("[Order Executor] 🛑 Lost leadership. Stopping order processing.")
                break

            try:
                response = self.stub.DequeueOrder(order_queue.DequeueRequest())
                if response.success:
                    order_id = response.order.order_id
                    logger.info(f"[Order Executor] ⚙️ Executing Order: {order_id}")
                    time.sleep(2)
                    logger.info(f"[Order Executor] ✅ Completed Order: {order_id}")
                else:
                    logger.debug("[Order Executor] 💤 No orders to process. Waiting...")
            except grpc.RpcError as e:
                logger.error(f"[Order Executor] ❌ gRPC error: {e}")

            time.sleep(POLL_INTERVAL)

    def monitor_leadership(self):
        """
        Monitor the leader election state and start/stop processing accordingly.
        """
        while self.running:
            if self.election.is_leader:
                if self.polling_thread is None or not self.polling_thread.is_alive():
                    self.polling_thread = threading.Thread(target=self.process_orders, daemon=True)
                    self.polling_thread.start()
            else:
                logger.info("[Order Executor] 🤝 Not the leader. Waiting...")
            time.sleep(5)

    def run(self):
        """
        Entry point to run election and monitor leadership status.
        """
        logger.info("[Order Executor] 🔄 Starting election and leadership monitor...")
        self.election.start()  # Combined check + heartbeat
        self.monitor_leadership()

def main():
    logger.info("[Order Executor] 🚀 Starting Order Executor...")

    # ✅ 新增启动 Election gRPC Server
    threading.Thread(target=start_election_server, daemon=True).start()

    executor = OrderExecutor()
    executor.run()

if __name__ == "__main__":
    main()
