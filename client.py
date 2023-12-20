# client.py
import asyncio
import websockets

async def process_data(): #We create users for server then print the info it gets from the server into the log.
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            response = await websocket.recv()
            print(f"Received from server: {response}")#It prints the message which is taken from server.(String)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(process_data())
