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
            self.clear_queue()
            with open("state.png", 'rb') as file:
                image_data = file.read()
            if not isinstance(image_data, bytes):
                # Ensure image_data is JSON-encoded if it's not already in bytes
                image_data = json.dumps(image_data).encode('utf-8')
            # Send the length of the image_data first (4 bytes)
            length = struct.pack('I', len(image_data))
            self.socket.send(length, zmq.SNDMORE)
            self.clear_queue()
            self.socket.send(image_data)
            self.clear_queue()
            return message
        
        except zmq.Again as e:
            print(f"Timeout or no message received: {e}")
            return None
        except zmq.ZMQError as e:
            print(f"Error receiving message: {e}")
            raise

    def close(self):
        try:
            self.socket.close()
            self.context.term()
            print("Server closed.")
        except zmq.ZMQError as e:
            print(f"Error closing socket or context: {e}")

    def clear_queue(self):
        while True:
            try:
                # Non-blocking receive to clear the queue
                message = self.socket.recv(flags=zmq.NOBLOCK)
                print(f"Cleared message: {message}")
            except zmq.Again:
                # No more messages; exit the loop
                break
            except zmq.ZMQError as e:
                print(f"Error while clearing socket queue: {e}")
                break