proto:
	python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. example.proto
run:
	SW_AGENT_COLLECTOR_BACKEND_SERVICES=127.0.0.1:11800 sw-python run python main.py