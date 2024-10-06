from concurrent import futures
from typing import Iterable

import grpc

import lecture_2.grpc_example.ping_pb2 as pb2
import lecture_2.grpc_example.ping_pb2_grpc as pb2_grpc


class PingPongService(pb2_grpc.PingPongServicer):
    def Ping(self, request: pb2.PingRequest, context):
        return pb2.PongResponce(message=request.message)
    
    def PingStream(self, request_iterator: Iterable[pb2.PingRequest], context):
        for message in request_iterator:
            yield pb2.PongResponce(message=message.message)


if __name__ == "__main__":
    print("Running gRPC PingPong server")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_PingPongServicer_to_server(PingPongService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()