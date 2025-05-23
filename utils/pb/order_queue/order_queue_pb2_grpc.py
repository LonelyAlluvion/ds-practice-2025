# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import order_queue_pb2 as order__queue__pb2


class OrderQueueStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.EnqueueOrder = channel.unary_unary(
                '/order_queue.OrderQueue/EnqueueOrder',
                request_serializer=order__queue__pb2.EnqueueRequest.SerializeToString,
                response_deserializer=order__queue__pb2.EnqueueResponse.FromString,
                )
        self.DequeueOrder = channel.unary_unary(
                '/order_queue.OrderQueue/DequeueOrder',
                request_serializer=order__queue__pb2.DequeueRequest.SerializeToString,
                response_deserializer=order__queue__pb2.DequeueResponse.FromString,
                )
        self.ClearOrderData = channel.unary_unary(
                '/order_queue.OrderQueue/ClearOrderData',
                request_serializer=order__queue__pb2.ClearOrderRequest.SerializeToString,
                response_deserializer=order__queue__pb2.ClearOrderResponse.FromString,
                )


class OrderQueueServicer(object):
    """Missing associated documentation comment in .proto file."""

    def EnqueueOrder(self, request, context):
        """Enqueue a new order
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DequeueOrder(self, request, context):
        """Dequeue an order (to be consumed by the leader/executor)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ClearOrderData(self, request, context):
        """Clear order data (optional cleanup)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_OrderQueueServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'EnqueueOrder': grpc.unary_unary_rpc_method_handler(
                    servicer.EnqueueOrder,
                    request_deserializer=order__queue__pb2.EnqueueRequest.FromString,
                    response_serializer=order__queue__pb2.EnqueueResponse.SerializeToString,
            ),
            'DequeueOrder': grpc.unary_unary_rpc_method_handler(
                    servicer.DequeueOrder,
                    request_deserializer=order__queue__pb2.DequeueRequest.FromString,
                    response_serializer=order__queue__pb2.DequeueResponse.SerializeToString,
            ),
            'ClearOrderData': grpc.unary_unary_rpc_method_handler(
                    servicer.ClearOrderData,
                    request_deserializer=order__queue__pb2.ClearOrderRequest.FromString,
                    response_serializer=order__queue__pb2.ClearOrderResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'order_queue.OrderQueue', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class OrderQueue(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def EnqueueOrder(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/order_queue.OrderQueue/EnqueueOrder',
            order__queue__pb2.EnqueueRequest.SerializeToString,
            order__queue__pb2.EnqueueResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DequeueOrder(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/order_queue.OrderQueue/DequeueOrder',
            order__queue__pb2.DequeueRequest.SerializeToString,
            order__queue__pb2.DequeueResponse.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/order_queue.OrderQueue/ClearOrderData',
            order__queue__pb2.ClearOrderRequest.SerializeToString,
            order__queue__pb2.ClearOrderResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
