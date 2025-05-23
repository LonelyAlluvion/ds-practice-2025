# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import election_pb2 as election__pb2


class ElectionServiceStub(object):
    """The ElectionService defines the RPC methods used for leader election between Order Executors.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.StartElection = channel.unary_unary(
                '/election.ElectionService/StartElection',
                request_serializer=election__pb2.ElectionRequest.SerializeToString,
                response_deserializer=election__pb2.ElectionResponse.FromString,
                )
        self.AnnounceLeader = channel.unary_unary(
                '/election.ElectionService/AnnounceLeader',
                request_serializer=election__pb2.LeaderAnnouncement.SerializeToString,
                response_deserializer=election__pb2.Ack.FromString,
                )
        self.Heartbeat = channel.unary_unary(
                '/election.ElectionService/Heartbeat',
                request_serializer=election__pb2.HeartbeatRequest.SerializeToString,
                response_deserializer=election__pb2.Ack.FromString,
                )


class ElectionServiceServicer(object):
    """The ElectionService defines the RPC methods used for leader election between Order Executors.
    """

    def StartElection(self, request, context):
        """Initiates a leader election process.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AnnounceLeader(self, request, context):
        """Broadcasts the elected leader to all other nodes.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Heartbeat(self, request, context):
        """Used by the leader to signal that it is still alive.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ElectionServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'StartElection': grpc.unary_unary_rpc_method_handler(
                    servicer.StartElection,
                    request_deserializer=election__pb2.ElectionRequest.FromString,
                    response_serializer=election__pb2.ElectionResponse.SerializeToString,
            ),
            'AnnounceLeader': grpc.unary_unary_rpc_method_handler(
                    servicer.AnnounceLeader,
                    request_deserializer=election__pb2.LeaderAnnouncement.FromString,
                    response_serializer=election__pb2.Ack.SerializeToString,
            ),
            'Heartbeat': grpc.unary_unary_rpc_method_handler(
                    servicer.Heartbeat,
                    request_deserializer=election__pb2.HeartbeatRequest.FromString,
                    response_serializer=election__pb2.Ack.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'election.ElectionService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ElectionService(object):
    """The ElectionService defines the RPC methods used for leader election between Order Executors.
    """

    @staticmethod
    def StartElection(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/election.ElectionService/StartElection',
            election__pb2.ElectionRequest.SerializeToString,
            election__pb2.ElectionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AnnounceLeader(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/election.ElectionService/AnnounceLeader',
            election__pb2.LeaderAnnouncement.SerializeToString,
            election__pb2.Ack.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Heartbeat(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/election.ElectionService/Heartbeat',
            election__pb2.HeartbeatRequest.SerializeToString,
            election__pb2.Ack.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
