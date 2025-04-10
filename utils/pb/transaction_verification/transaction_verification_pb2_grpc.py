# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import transaction_verification_pb2 as transaction__verification__pb2


class TransactionVerificationStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.VerifyTransaction = channel.unary_unary(
                '/transaction_verification.TransactionVerification/VerifyTransaction',
                request_serializer=transaction__verification__pb2.TransactionRequest.SerializeToString,
                response_deserializer=transaction__verification__pb2.TransactionResponse.FromString,
                )
<<<<<<< HEAD
=======
        self.ClearOrderData = channel.unary_unary(
                '/transaction_verification.TransactionVerification/ClearOrderData',
                request_serializer=transaction__verification__pb2.ClearOrderRequest.SerializeToString,
                response_deserializer=transaction__verification__pb2.ClearOrderResponse.FromString,
                )
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)


class TransactionVerificationServicer(object):
    """Missing associated documentation comment in .proto file."""

    def VerifyTransaction(self, request, context):
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

def add_TransactionVerificationServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'VerifyTransaction': grpc.unary_unary_rpc_method_handler(
                    servicer.VerifyTransaction,
                    request_deserializer=transaction__verification__pb2.TransactionRequest.FromString,
                    response_serializer=transaction__verification__pb2.TransactionResponse.SerializeToString,
            ),
<<<<<<< HEAD
=======
            'ClearOrderData': grpc.unary_unary_rpc_method_handler(
                    servicer.ClearOrderData,
                    request_deserializer=transaction__verification__pb2.ClearOrderRequest.FromString,
                    response_serializer=transaction__verification__pb2.ClearOrderResponse.SerializeToString,
            ),
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'transaction_verification.TransactionVerification', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class TransactionVerification(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def VerifyTransaction(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/transaction_verification.TransactionVerification/VerifyTransaction',
            transaction__verification__pb2.TransactionRequest.SerializeToString,
            transaction__verification__pb2.TransactionResponse.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/transaction_verification.TransactionVerification/ClearOrderData',
            transaction__verification__pb2.ClearOrderRequest.SerializeToString,
            transaction__verification__pb2.ClearOrderResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
