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
        self.clear_queue()
        length_msg = self.socket.recv()
        length = int.from_bytes(length_msg, byteorder='big')
        # Receive the actual data in chunks
        image_data = b''
        image_data += self.socket.recv()
        # Save the received data to a file
        with open("receive.png", 'wb') as file:
            file.write(image_data)
    
    def disconnect(self):
        self.socket.close()
        self.context.term()
    
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