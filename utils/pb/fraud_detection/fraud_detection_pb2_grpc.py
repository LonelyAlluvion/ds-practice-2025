# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import fraud_detection_pb2 as fraud__detection__pb2


class FraudDetectionStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CheckFraud = channel.unary_unary(
                '/fraud_detection.FraudDetection/CheckFraud',
                request_serializer=fraud__detection__pb2.FraudRequest.SerializeToString,
                response_deserializer=fraud__detection__pb2.FraudResponse.FromString,
                )
        self.ClearOrderData = channel.unary_unary(
                '/fraud_detection.FraudDetection/ClearOrderData',
                request_serializer=fraud__detection__pb2.ClearOrderRequest.SerializeToString,
                response_deserializer=fraud__detection__pb2.ClearOrderResponse.FromString,
                )


class FraudDetectionServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CheckFraud(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ClearOrderData(self, request, context):
        """新增清理订单方法
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FraudDetectionServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CheckFraud': grpc.unary_unary_rpc_method_handler(
                    servicer.CheckFraud,
                    request_deserializer=fraud__detection__pb2.FraudRequest.FromString,
                    response_serializer=fraud__detection__pb2.FraudResponse.SerializeToString,
            ),
            'ClearOrderData': grpc.unary_unary_rpc_method_handler(
                    servicer.ClearOrderData,
                    request_deserializer=fraud__detection__pb2.ClearOrderRequest.FromString,
                    response_serializer=fraud__detection__pb2.ClearOrderResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'fraud_detection.FraudDetection', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class FraudDetection(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CheckFraud(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/fraud_detection.FraudDetection/CheckFraud',
            fraud__detection__pb2.FraudRequest.SerializeToString,
            fraud__detection__pb2.FraudResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ClearOrderData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/fraud_detection.FraudDetection/ClearOrderData',
            fraud__detection__pb2.ClearOrderRequest.SerializeToString,
            fraud__detection__pb2.ClearOrderResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
