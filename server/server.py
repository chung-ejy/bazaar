import zmq
import json

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

    def receive(self):
        try:
            # Receive raw bytes
            message_bytes = self.socket.recv()
            # Decode bytes to JSON
            message = json.loads(message_bytes.decode('utf-8'))
            # Send a JSON response
            response = {'status': 'success', 'data': message}
            self.socket.send_json(response)
            return message
        except zmq.Again as e:
            return {}
        except zmq.ZMQError as e:
            raise
        except json.JSONDecodeError as e:
            # Send an error response for invalid JSON
            response = {'status': 'error', 'message': 'Invalid JSON'}
            self.socket.send_json(response)
    
    def send(self, data):
        try:
            # Convert data to JSON and encode as bytes
            json_data = json.dumps(data)
            json_bytes = json_data.encode('utf-8')
            self.socket.send(json_bytes)
            message_bytes = self.socket.recv()
            # Decode bytes to JSON
            message = json.loads(message_bytes.decode('utf-8'))
            # Send a JSON response
            response = {'status': 'success', 'data': message}
            # print(response)
        except zmq.ZMQError as e:
            raise
        except json.JSONEncodeError as e:
            print(f"Error encoding JSON: {e}")
    
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