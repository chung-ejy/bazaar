import zmq

class Client:

    def __init__(self, host='tcp://127.0.0.1', port='65432'):
        self.host = host
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
    
    def connect(self):
        self.socket.connect(f"{self.host}:{self.port}")
    
    def send(self, message):        
        # Send a request (message) to the server
        self.socket.send_string(message)
        print(self.socket.recv_string())
    
    def receive(self):
        try:
            # Receive the length of the data (4 bytes)
            length_msg = self.socket.recv()
            length = int.from_bytes(length_msg, byteorder='big')
            
            # Receive the actual data in chunks
            image_data = b''
            while len(image_data) < length:
                try:
                    # Use flags if provided, otherwise default to blocking
                    image_data += self.socket.recv()
                except zmq.Again as e:
                    print(f"Timeout or no message received: {e}")
                    return None
                except zmq.ZMQError as e:
                    print(f"Error receiving message: {e}")
                    raise  
            # Save the received data to a file
            with open("receive.png", 'wb') as file:
                file.write(image_data)
        except Exception as e:
            print(f"Error receiving data: {e}")
    
    def disconnect(self):
        self.socket.close()
        self.context.term()
