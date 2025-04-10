import grpc
import threading
import time
import socket
import logging
import sys
import os

# === gRPC Path Setup ===
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
election_pb_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/election'))
sys.path.insert(0, election_pb_path)

import election_pb2
import election_pb2_grpc

# === Logging Configuration ===
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ElectionClient")

# === Config ===
ELECTION_PORT = os.getenv("ELECTION_PORT", "50055")
ELECTION_HOST = os.getenv("ELECTION_HOST", socket.gethostname())
EXECUTOR_ID = os.getenv("EXECUTOR_ID", socket.gethostname())
EXECUTOR_PRIORITY = int(os.getenv("EXECUTOR_PRIORITY", "0"))
HEARTBEAT_INTERVAL = 3
PEER_LIST = os.getenv("ELECTION_PEERS", "").split(",")

class ElectionClient:
    def __init__(self):
        self.channel = grpc.insecure_channel(f"{ELECTION_HOST}:{ELECTION_PORT}")
        self.stub = election_pb2_grpc.ElectionServiceStub(self.channel)
        self.executor_id = EXECUTOR_ID
        self.priority = EXECUTOR_PRIORITY
        self.heartbeat_interval = HEARTBEAT_INTERVAL
        self.leader_id = None
        self.is_leader = False
        self.heartbeat_thread = None
        self.monitor_thread = None
        self.running = True
        self.peer_list = PEER_LIST

    def start_election(self):
        logger.info(f"[ElectionClient] 📣 Starting election from {self.executor_id} (priority={self.priority})")

        responses = []
        for peer in self.peer_list:
            if peer.strip() == "" or peer.strip().startswith(self.executor_id):  # ✅ 跳过向自己发请求
                continue
            try:
                channel = grpc.insecure_channel(peer)
                stub = election_pb2_grpc.ElectionServiceStub(channel)
                request = election_pb2.ElectionRequest(executor_id=self.executor_id, priority=self.priority)
                response = stub.StartElection(request)
                responses.append(response.ok)
                if response.ok:
                    logger.info(f"[ElectionClient] ❌ Peer {peer} rejected my leadership (higher or equal priority).")
            except grpc.RpcError as e:
                logger.warning(f"[ElectionClient] ⚠️ Failed to contact {peer} during election: {e}")
                responses.append(False)

        if not any(responses):  # ✅ 没有人反对
            self.leader_id = self.executor_id
            self.is_leader = True
            self.announce_leadership()
        else:
            self.is_leader = False
            self.leader_id = None

        logger.info(f"[ElectionClient] 🗳️ Election result — I am leader: {self.is_leader}")
        return self.leader_id

    def announce_leadership(self):
        for peer in self.peer_list:
            if peer.strip() == "" or peer.strip().startswith(self.executor_id):
                continue
            try:
                channel = grpc.insecure_channel(peer)
                stub = election_pb2_grpc.ElectionServiceStub(channel)
                request = election_pb2.LeaderAnnouncement(leader_id=self.executor_id)
                stub.AnnounceLeader(request)
                logger.info(f"[ElectionClient] 📢 Announced leadership to {peer}")
            except grpc.RpcError as e:
                logger.warning(f"[ElectionClient] ⚠️ Failed to announce leader to {peer}: {e}")

    def send_heartbeat(self):
        while self.is_leader and self.running:
            for peer in self.peer_list:
                if peer.strip() == "" or peer.strip().startswith(self.executor_id):
                    continue
                try:
                    channel = grpc.insecure_channel(peer)
                    stub = election_pb2_grpc.ElectionServiceStub(channel)
                    request = election_pb2.HeartbeatRequest(executor_id=self.executor_id)
                    response = stub.Heartbeat(request)
                    if not response.success:
                        logger.warning(f"[ElectionClient] ⚠️ Heartbeat to {peer} failed")
                    else:
                        logger.debug(f"[ElectionClient] ❤️ Heartbeat sent successfully to {peer}")
                except grpc.RpcError as e:
                    logger.error(f"[ElectionClient] ❌ Heartbeat error to {peer}: {e}")
            time.sleep(self.heartbeat_interval)

    def start_heartbeat_loop(self):
        if self.is_leader:
            logger.info("[ElectionClient] 🔁 Starting heartbeat loop as leader")
            self.heartbeat_thread = threading.Thread(target=self.send_heartbeat, daemon=True)
            self.heartbeat_thread.start()

    def monitor_leader_health(self):
        while self.running:
            if not self.is_leader and self.leader_id:
                logger.debug("[ElectionClient] 🔍 Monitoring leader health...")
                try:
                    request = election_pb2.HeartbeatRequest(executor_id=self.leader_id)
                    response = self.stub.Heartbeat(request)
                    if not response.success:
                        logger.warning("[ElectionClient] 💔 Leader heartbeat failed. Triggering re-election.")
                        self.check_or_elect_leader()
                except grpc.RpcError:
                    logger.warning("[ElectionClient] ❌ Leader unreachable. Triggering re-election.")
                    self.check_or_elect_leader()
            time.sleep(self.heartbeat_interval * 2)

    def check_or_elect_leader(self):
        elected_leader = self.start_election()
        if elected_leader:
            if self.is_leader:
                self.start_heartbeat_loop()
                logger.info(f"[ElectionClient] 🏆 I am the new leader: {self.executor_id}")
            else:
                logger.info(f"[ElectionClient] 🤝 I am follower, leader is {self.leader_id}")
        else:
            logger.warning("[ElectionClient] ⚠️ Election failed. No leader elected.")

    def start_monitoring(self):
        logger.info("[ElectionClient] 👁️ Starting leader monitoring...")
        self.monitor_thread = threading.Thread(target=self.monitor_leader_health, daemon=True)
        self.monitor_thread.start()

    def start(self):
        logger.info("[ElectionClient] 💤 Waiting for all peers to be up...")
        time.sleep(5)
        self.check_or_elect_leader()
        self.start_monitoring()
