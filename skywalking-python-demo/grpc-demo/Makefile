proto:
	python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. example.proto

server:
	SW_PLUGIN_GRPC_IGNORED_METHODS=/example.Greeter/SayHelloSS SW_AGENT_COLLECTOR_BACKEND_SERVICES=127.0.0.1:11800 sw-python -d run python server.py

aio.server:
	SW_PLUGIN_GRPC_IGNORED_METHODS=/example.Greeter/SayHelloUS,/example.Greeter/SayHelloSS SW_AGENT_COLLECTOR_BACKEND_SERVICES=127.0.0.1:11800 sw-python -d run python aio_s.py

client:
	SW_PLUGIN_GRPC_IGNORED_METHODS=/example.Greeter/SayHelloUS,/example.Greeter/SayHelloSS SW_AGENT_COLLECTOR_BACKEND_SERVICES=127.0.0.1:11800 sw-python -d run python client.py

aio.client:
	SW_PLUGIN_GRPC_IGNORED_METHODS=/example.Greeter/SayHelloUS,/example.Greeter/SayHelloSS SW_AGENT_COLLECTOR_BACKEND_SERVICES=127.0.0.1:11800 sw-python -d run python aio_c.py

