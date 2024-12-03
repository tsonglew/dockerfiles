import socketserver
from concurrent import futures
from http.server import BaseHTTPRequestHandler

import grpc

import example_pb2
import example_pb2_grpc


def generate_messages():
    yield example_pb2.HelloRequest(name=f"World, World")


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        channel = grpc.intercept_channel(grpc.insecure_channel("127.0.0.1:50051"))
        stub = example_pb2_grpc.GreeterStub(channel)
        request = example_pb2.HelloRequest(name="World")
        stub.SayHello(request)
        for _ in stub.SayHelloUS(request):
            pass
        stub.SayHelloSU(generate_messages())
        for _ in stub.SayHelloSS(generate_messages()):
            pass
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello, world")


if __name__ == "__main__":
    PORT = 50002
    with socketserver.TCPServer(("", PORT), SimpleHTTPRequestHandler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()
