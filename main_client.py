from client.client import Client

if __name__ == "__main__":   
    client = Client()
    client.connect()
    message = input().strip()
    client.send_request_to_server(message)
    client.disconnect()
