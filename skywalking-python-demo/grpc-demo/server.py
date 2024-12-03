from concurrent import futures

import grpc

import example_pb2
import example_pb2_grpc


class GreeterServicer(example_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return example_pb2.HelloReply()

    def SayHelloUS(self, request, context):
        for i in range(3):
            response = example_pb2.HelloReply()
            response.message = f"Hello, {request.name} {i}!"
            yield response

    def SayHelloSU(self, request_iterator, context):
        response = example_pb2.HelloReply()
        for request in request_iterator:
            response.message = f"Hello, {request.name}!"
        return response

    def SayHelloSS(self, request_iterator, context):
        for i, request in enumerate(request_iterator):
            response = example_pb2.HelloReply()
            response.message = f"Hello, {request.name} {i}!"
            yield response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    example_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
