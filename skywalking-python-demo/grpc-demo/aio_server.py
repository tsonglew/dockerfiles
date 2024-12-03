import grpc.aio

import example_pb2
import example_pb2_grpc


async def hello1():
    # Asynchronously establish a connection to the server
    async with grpc.aio.insecure_channel("127.0.0.1:50051") as channel:
        # Create an asynchronous stub (client)
        stub = example_pb2_grpc.GreeterStub(channel)

        # Create a HelloRequest message
        request = example_pb2.HelloRequest(name="World")

        # Use 'await' for the asynchronous RPC call
        response = await stub.SayHello1(request)

    # Print the received message from the server
    print(f"hello1 Received message: {response.message}")


async def hello2():
    # Asynchronously establish a connection to the server
    async with grpc.aio.insecure_channel("127.0.0.1:50051") as channel:
        # Create an asynchronous stub (client)
        stub = example_pb2_grpc.GreeterStub(channel)

        # Create a HelloRequest message
        request = example_pb2.HelloRequest(name="World")

        # Use 'await' for the asynchronous RPC call
        response = await stub.SayHello2(request)

    # Print the received message from the server
    print(f"hello2 Received message: {response.message}")


class GreeterServicer(example_pb2_grpc.GreeterServicer):
    async def SayHello(self, request, context):
        await asyncio.sleep(1)
        await hello1()
        response = example_pb2.HelloReply()
        response.message = f"Hello, {request.name}!"
        return response

    async def SayHello1(self, request, context):
        await asyncio.sleep(1)
        response = example_pb2.HelloReply()
        response.message = f"Hello, {request.name}!"
        return response

    async def SayHello2(self, request, context):
        await asyncio.sleep(1)
        response = example_pb2.HelloReply()
        response.message = f"Hello, {request.name}!"
        return response

    async def SayHelloSS(self, request_iterator, context):
        async for request in request_iterator:
            response = example_pb2.HelloReply()
            response.message = f"Hello, {request.name}!"
            yield response

    async def SayHelloSU(self, request_iterator, context):
        async for request in request_iterator:
            await asyncio.sleep(1)
        response = example_pb2.HelloReply()
        response.message = f"Hello, su!"
        return response

    async def SayHelloUS(self, request, context):
        response = example_pb2.HelloReply()
        response.message = f"Hello, us!"
        for i in range(3):
            await asyncio.sleep(1)
            yield response


async def serve():
    # Create an asynchronous server
    server = grpc.aio.server()
    example_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    print("gRPC server running on port 50051")
    await server.wait_for_termination()


if __name__ == "__main__":
    import asyncio

    asyncio.run(serve())
