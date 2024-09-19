from client.client import Client
import sys
if __name__ == "__main__":   
    client = Client("127.0.0.1","65432")
    client.connect()
    while True:
        try:
            message = input()
            if message == "exit":
                sys.exit()
            client.send(message)
        except Exception as e:
            print(str(e))
    client.disconnect()
