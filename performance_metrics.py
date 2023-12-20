# performance_metrics.py
import asyncio
import websockets
import time
import psutil  # For monitoring system resources

async def measure_latency():  # This function is for testing the latency of the server
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        start_time = time.time()
        await websocket.recv()
        latency = time.time() - start_time
        print(f"Latency: {latency:.15f} seconds")

async def measure_throughput(messages_to_send):  # This function is for testing the data amount that the server can handle
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        start_time = time.time()
        total_data_size = 0  # Track the total size of data sent

        for _ in range(messages_to_send):
            data = "Performance Test Message"
            await websocket.send(data)
            total_data_size += len(data)  # Add the size of the current data to the total
            # await websocket.recv()  # Commented out to keep the connection open

        elapsed_time = time.time() - start_time
        throughput = messages_to_send / elapsed_time
        print(f"Throughput: {throughput:.4f} messages per second")
        print(f"Total Data Size: {total_data_size} bytes")
        print(f"Time Spent: {elapsed_time:.2f} seconds")

async def measure_resource_utilization():  # This function is for getting machine resource utilization information
    while True:
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        print(f"CPU Usage: {cpu_percent}% | Memory Usage: {memory_percent}%")
        await asyncio.sleep(5)  # Adjust the interval as needed

async def measure_scalability(num_clients, messages_per_client):  # This function is for testing the amount of users and messages
    print(f"\nScalability Test: {num_clients} clients will try to take {messages_per_client} messages each. Please wait...\n")
    async def simulate_client(client_id):
        uri = "ws://localhost:8765"
        async with websockets.connect(uri) as websocket:
            print(f"Client {client_id} connected.")
            for _ in range(messages_per_client):
                await websocket.send(f"Client {client_id} Message")
                await websocket.recv()  # Commented out to keep the connection open
            print(f"Client {client_id} completed.")

    start_time = time.time()  # Record the start time
    tasks = [simulate_client(i) for i in range(num_clients)]
    await asyncio.gather(*tasks)
    elapsed_time = time.time() - start_time
    print(f"\nScalability Test Completed in {elapsed_time:.2f} seconds. Testing is over!")

async def main():
    print("Running Latency Measurement:")
    await measure_latency()  # this function will give us information about latency

    print("\nRunning Throughput Measurement please wait:")
    await measure_throughput(10000)  # We can increase or decrease this number for testing more data or less.

    print("\nRunning Resource Utilization Measurement please wait:")  # it will give us machine resource utilization information
    resource_task = asyncio.create_task(measure_resource_utilization())
    await asyncio.sleep(15)
    resource_task.cancel()

    print("\nRunning Scalability Test please wait:")
    await measure_scalability(num_clients=100, messages_per_client=20)  # We test server scalability here with connecting with more clients at a time.

if __name__ == "__main__":
    asyncio.run(main())
