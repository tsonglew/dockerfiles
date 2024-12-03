import asyncio

import grpc.aio

import example_pb2
import example_pb2_grpc


async def generate_requests():
    names = ["Alice", "Bob", "Charlie"]
    for name in names:
        yield example_pb2.HelloRequest(name=name)
        await asyncio.sleep(1)  # Simulating delay


class UUInterceptor(grpc.aio.UnaryUnaryClientInterceptor):

    async def intercept_unary_unary(self, continuation, client_call_details, request):
        print(f"client_call_details: {client_call_details}")
        print(f"request: {request}")
        response = await continuation(client_call_details, request)
        print(f"response: {response}")
        return response


async def run():
    # Asynchronously establish a connection to the server
    # async with grpc.aio.insecure_channel("127.0.0.1:50051", interceptors=[UUInterceptor()]) as channel:
    async with grpc.aio.insecure_channel("127.0.0.1:50051") as channel:
        # Apply the interceptor
        # Create an asynchronous stub (client)
        stub = example_pb2_grpc.GreeterStub(channel)

        # Create a HelloRequest message
        request = example_pb2.HelloRequest(name="World")

        # Asynchronously make the RPC call using 'await'
        response = await stub.SayHello(request)
        # async for resp in stub.SayHelloSS(generate_requests()):
        #     print(f"Received message: {resp.message}")
        async for resp in stub.SayHelloUS(example_pb2.HelloRequest(name="World")):
            print(f"Received message: {resp.message}")
        resp = await stub.SayHelloSU(generate_requests())
        async for resp in stub.SayHelloSS(generate_requests()):
            print(f"Received message: {resp.message}")
        # resp = await stub.SayHello(example_pb2.HelloRequest(name="World"))

    await asyncio.sleep(10)

    # Print the received message from the server
    # print(f"Received message: {response.message}")


if __name__ == "__main__":
    asyncio.run(run())
