import zmq
import json
import struct
class Server:

    def __init__(self, host='tcp://127.0.0.1', port='65432'):
        self.host = host
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.setsockopt(zmq.RCVTIMEO, 5000)  # 5-second timeout for receive operations

    def start_server(self):
        try:
            self.socket.bind(f"{self.host}:{self.port}")
            print(f"Server listening on {self.host}:{self.port}")
        except zmq.ZMQError as e:
            print(f"Error starting server: {e}")
            raise

    def receive(self, flags=0):
        try:
            # Use flags if provided, otherwise default to blocking
            message = self.socket.recv_string(flags)
            print(f"Received request: {message}")
            self.socket.send_string("success")
            return message
        except zmq.Again as e:
            print(f"Timeout or no message received: {e}")
            return None
        except zmq.ZMQError as e:
            print(f"Error receiving message: {e}")
            raise

    def send(self, data):
        try:
            if not isinstance(data, bytes):
                # Ensure data is JSON-encoded if it's not already in bytes
                data = json.dumps(data).encode('utf-8')
            # Send the length of the data first (4 bytes)
            length = struct.pack('I', len(data))
            self.socket.send(length, zmq.SNDMORE)
            # Send data to the client
            self.socket.send(data)
        except zmq.ZMQError as e:
            print(f"Error sending message: {e}")
            raise

    def close(self):
        try:
            self.socket.close()
            self.context.term()
            print("Server closed.")
        except zmq.ZMQError as e:
            print(f"Error closing socket or context: {e}")
