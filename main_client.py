from client.client import Client
import sys
if __name__ == "__main__":   
    client = Client()
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
