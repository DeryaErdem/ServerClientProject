# server.py
import asyncio
import websockets

connected_clients = set()  # Maintain a set to track connected clients

async def stream_data(websocket, path): #data stream function
    connected_clients.add(websocket)  # Add the new client to the set whenever a new client connects to the server
    print(f"New client connected. Total clients: {len(connected_clients)}") #To be able to see the clients in the server. We print it into the log.

    count = 0 #we create a variable in order to track the unique messages for clients. Every client takes messages as data point : 0 first and it increase overrtime
    try:
        while websocket.open: #it opens the server
            data = f"Data Point {count}"
            await websocket.send(data)
            count += 1
            await asyncio.sleep(1)  # Stream data every 1 second we can send it faster if needed
    except websockets.exceptions.ConnectionClosedOK: #We do not take thsese error often but they are here for safety.
        print("Client closed the connection")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Client encountered an error or closed unexpectedly: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        connected_clients.remove(websocket)  # Remove the disconnected client from the set
        print(f"Closing the server connection. Remaining clients: {len(connected_clients)}") #if there is no error while client leaving the server we print this log message.

if __name__ == "__main__":
    print("WebSocket server started. Waiting for connections...")#when we run the python file we take this message as first log
    start_server = websockets.serve(stream_data, "localhost", 8765)#we start it at a local host

    try:
        asyncio.get_event_loop().run_until_complete(start_server)#it starts the server until it gets closed by keyboard input which is (ctrl+c)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print("Server manually terminated.")
    finally:
        start_server.close()
        asyncio.get_event_loop().run_until_complete(start_server.wait_closed())
