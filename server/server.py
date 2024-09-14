import zmq

class Server:

    def __init__(self,host='tcp://127.0.0.1', port='65432'):
        self.host = host
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)

    def start_server(self):

        self.socket.bind(f"{self.host}:{self.port}")
        
        print(f"Server listening on {self.host}:{self.port}")
    
    def receive(self):
        # Wait to receive a request from the client
        message = self.socket.recv_string()
        print(f"Received request: {message}")
        
        # Process the request and send a response
        response = f"Echoing your request: {message}"
        self.socket.send_string(response)
        return message