from file_xor import roxe
from file_xor.StreamServer import levanter as server
import threading
import asyncio

def start_server():
    # Create a new event loop for the thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(server.serve())

if __name__ == "__main__":
    # Run server in a separate thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Keep roxe bot running
    roxe.run()
