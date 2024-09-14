from client.client import Client

if __name__ == "__main__":   
    client = Client()
    client.connect()
    while True:
        try:
            message = input().strip()
            client.send_request_to_server(message)
        except Exception as e:
            print(str(e))
    client.disconnect()
