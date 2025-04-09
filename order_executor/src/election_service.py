import grpc
import logging
import time
import threading
import os
import sys
from concurrent import futures

# === Configure logging ===
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# === Load gRPC definitions ===
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
election_pb_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/election'))
sys.path.insert(0, election_pb_path)

import election_pb2 as election
import election_pb2_grpc

# === Configuration ===
EXECUTOR_ID = os.getenv("EXECUTOR_ID", f"executor-{int(time.time())}")
EXECUTOR_PRIORITY = int(os.getenv("EXECUTOR_PRIORITY", "0"))
PORT = os.getenv("ELECTION_PORT", "50060")
HEARTBEAT_TIMEOUT = 10  # seconds


class ElectionServiceServicer(election_pb2_grpc.ElectionServiceServicer):
    def __init__(self):
        self.current_leader = None
        self.last_heartbeat = time.time()

        # 启动 heartbeat 监控线程
        self.monitor_thread = threading.Thread(target=self.monitor_leader_liveness, daemon=True)
        self.monitor_thread.start()

    def StartElection(self, request, context):
        """
        Handles election requests from other executors.
        Accepts or denies based on executor priority.
        """
        logger.info(f"[Election] ✅ Received election request from {request.executor_id} with priority {request.priority}")

        if request.priority <= EXECUTOR_PRIORITY:
            logger.info(
                f"[Election] ❌ Denying election from {request.executor_id}, my priority ({EXECUTOR_PRIORITY}) is higher or equal")
            return election.ElectionResponse(ok=True)  # 告诉发起者“我不支持你”
        else:
            logger.info(f"[Election] ✅ Accepting election from {request.executor_id}, their priority is higher")
            self.current_leader = request.executor_id
            self.last_heartbeat = time.time()
            return election.ElectionResponse(ok=False)

    def AnnounceLeader(self, request, context):
        """
        Receives leader announcement and updates local state.
        """
        self.current_leader = request.leader_id
        self.last_heartbeat = time.time()
        logger.info(f"[Election] 📢 New leader announced: {self.current_leader}")
        return election.Ack(success=True)

    def Heartbeat(self, request, context):
        """
        Handles heartbeat from the current leader.
        """
        if self.current_leader is None:
            self.current_leader = request.executor_id
            self.last_heartbeat = time.time()
            logger.info(f"[Election] 🆕 Accepted first heartbeat, new leader is {self.current_leader}")
            return election.Ack(success=True)

        if request.executor_id == self.current_leader:
            self.last_heartbeat = time.time()
            logger.debug(f"[Election] ❤️ Heartbeat received from leader {request.executor_id}")
            return election.Ack(success=True)
        else:
            logger.warning(f"[Election] ⚠️ Heartbeat from unknown leader: {request.executor_id}")
            return election.Ack(success=False)

    def monitor_leader_liveness(self):
        """
        Monitors heartbeat timestamps to detect leader failure.
        """
        while True:
            if self.current_leader:
                elapsed = time.time() - self.last_heartbeat
                if elapsed > HEARTBEAT_TIMEOUT:
                    logger.warning(f"[Election] 💔 Leader {self.current_leader} is considered dead (no heartbeat in {elapsed:.1f}s)")
                    self.current_leader = None
            time.sleep(2)


def serve():
    """
    Starts the Election gRPC server.
    """
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        election_service = ElectionServiceServicer()
        election_pb2_grpc.add_ElectionServiceServicer_to_server(election_service, server)
        server.add_insecure_port(f"[::]:{PORT}")

        logger.info(f"[Election] 🚀 Election service running on port {PORT} (Executor ID: {EXECUTOR_ID}, Priority: {EXECUTOR_PRIORITY})")

        server.start()
        server.wait_for_termination()
    except Exception as e:
        logger.exception(f"[Election] ❌ Failed to start gRPC server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    serve()
