import asyncio
import socketserver
from http.server import BaseHTTPRequestHandler

import grpc

import example_pb2
import example_pb2_grpc


async def generate_messages():
    yield example_pb2.HelloRequest(name="World")


async def generate_requests():
    names = ["Alice", "Bob", "Charlie"]
    for name in names:
        yield example_pb2.HelloRequest(name=name)
        await asyncio.sleep(1)  # Simulating delay


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):  # noqa
        async def task():
            async with grpc.aio.insecure_channel("127.0.0.1:20061") as channel:
                stub = example_pb2_grpc.GreeterStub(channel)
                request = example_pb2.HelloRequest(name="World")
                await stub.SayHello(request)
                async for _ in stub.SayHelloUS(request):
                    pass
                await stub.SayHelloSU(generate_messages())
                async for _ in stub.SayHelloSS(generate_requests()):
                    pass

        asyncio.run(task())
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello, world")


if __name__ == "__main__":
    PORT = 20063
    with socketserver.TCPServer(("", PORT), SimpleHTTPRequestHandler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()
