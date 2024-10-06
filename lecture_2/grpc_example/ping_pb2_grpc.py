# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import ping_pb2 as ping__pb2

GRPC_GENERATED_VERSION = '1.66.2'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + ' but the generated code in ping_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class PingPongStub(object):
    """define a service
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Ping = channel.unary_unary(
                '/grpc_example.PingPong/Ping',
                request_serializer=ping__pb2.PingRequest.SerializeToString,
                response_deserializer=ping__pb2.PongResponce.FromString,
                _registered_method=True)
        self.PingStream = channel.stream_stream(
                '/grpc_example.PingPong/PingStream',
                request_serializer=ping__pb2.PingRequest.SerializeToString,
                response_deserializer=ping__pb2.PongResponce.FromString,
                _registered_method=True)


class PingPongServicer(object):
    """define a service
    """

    def Ping(self, request, context):
        """define an rpc method
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PingStream(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PingPongServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Ping': grpc.unary_unary_rpc_method_handler(
                    servicer.Ping,
                    request_deserializer=ping__pb2.PingRequest.FromString,
                    response_serializer=ping__pb2.PongResponce.SerializeToString,
            ),
            'PingStream': grpc.stream_stream_rpc_method_handler(
                    servicer.PingStream,
                    request_deserializer=ping__pb2.PingRequest.FromString,
                    response_serializer=ping__pb2.PongResponce.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'grpc_example.PingPong', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('grpc_example.PingPong', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class PingPong(object):
    """define a service
    """

    @staticmethod
    def Ping(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/grpc_example.PingPong/Ping',
            ping__pb2.PingRequest.SerializeToString,
            ping__pb2.PongResponce.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def PingStream(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(
            request_iterator,
            target,
            '/grpc_example.PingPong/PingStream',
            ping__pb2.PingRequest.SerializeToString,
            ping__pb2.PongResponce.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
