
import zmq

class Client:

    def __init__(self,host='tcp://127.0.0.1', port='65432'):
        self.host = host
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        
    def connect(self):
        self.socket.connect(f"{self.host}:{self.port}")
        print("connected")
    
    def send_request_to_server(self, message):        
        # Send a request (message) to the server
        print(f"Sending request: {message}")
        self.socket.send_string(message)
        
        # Wait for the server's reply
        reply = self.socket.recv_string()
        print(f"Received reply from server: {reply}")
    
    def disconnect(self):
        self.socket.close()
        self.context.term()
