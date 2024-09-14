import sys
from app.app import App

if __name__ == "__main__":
    app = App()
    try:
        app.run()
    except KeyboardInterrupt:
        print("Shutting down...")
        sys.exit(0)
