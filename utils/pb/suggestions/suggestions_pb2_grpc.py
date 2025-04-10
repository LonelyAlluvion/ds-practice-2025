# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import suggestions_pb2 as suggestions__pb2


class SuggestionsStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RecommendBooks = channel.unary_unary(
                '/suggestions.Suggestions/RecommendBooks',
                request_serializer=suggestions__pb2.RecommendationRequest.SerializeToString,
                response_deserializer=suggestions__pb2.RecommendationResponse.FromString,
                )
<<<<<<< HEAD
=======
        self.ClearOrderData = channel.unary_unary(
                '/suggestions.Suggestions/ClearOrderData',
                request_serializer=suggestions__pb2.ClearOrderRequest.SerializeToString,
                response_deserializer=suggestions__pb2.ClearOrderResponse.FromString,
                )
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)


class SuggestionsServicer(object):
    """Missing associated documentation comment in .proto file."""

    def RecommendBooks(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

<<<<<<< HEAD
=======
    def ClearOrderData(self, request, context):
        """新增清理订单方法
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)

def add_SuggestionsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RecommendBooks': grpc.unary_unary_rpc_method_handler(
                    servicer.RecommendBooks,
                    request_deserializer=suggestions__pb2.RecommendationRequest.FromString,
                    response_serializer=suggestions__pb2.RecommendationResponse.SerializeToString,
            ),
<<<<<<< HEAD
=======
            'ClearOrderData': grpc.unary_unary_rpc_method_handler(
                    servicer.ClearOrderData,
                    request_deserializer=suggestions__pb2.ClearOrderRequest.FromString,
                    response_serializer=suggestions__pb2.ClearOrderResponse.SerializeToString,
            ),
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'suggestions.Suggestions', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Suggestions(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def RecommendBooks(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/suggestions.Suggestions/RecommendBooks',
            suggestions__pb2.RecommendationRequest.SerializeToString,
            suggestions__pb2.RecommendationResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
<<<<<<< HEAD
=======

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
        return grpc.experimental.unary_unary(request, target, '/suggestions.Suggestions/ClearOrderData',
            suggestions__pb2.ClearOrderRequest.SerializeToString,
            suggestions__pb2.ClearOrderResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
