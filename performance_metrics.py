# performance_metrics.py
import asyncio
import websockets
import time
import psutil  # For monitoring system resources

async def measure_latency():#This function is for testing the latency of server
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        start_time = time.time()
        await websocket.recv()
        latency = time.time() - start_time
        print(f"Latency: {latency:.15f} seconds")

async def measure_throughput(messages_to_send):#This function is for testing the data amount that server can handle
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

async def measure_resource_utilization():#This function is for getting the machine resource utilization information.
    while True:
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        print(f"CPU Usage: {cpu_percent}% | Memory Usage: {memory_percent}%")
        await asyncio.sleep(5)  # Adjust the interval as needed

async def measure_scalability(num_clients, messages_per_client, duration_seconds): #This function is for testing the amount of user and messages
    print(f"\nScalability Test: {num_clients} clients will try to take {messages_per_client} messages each. Please wait...\n")
    async def simulate_client(client_id):                                          #they take from the server without crashing it.
        uri = "ws://localhost:8765"
        async with websockets.connect(uri) as websocket:
            print(f"Client {client_id} connected.")
            for _ in range(messages_per_client):
                await websocket.send(f"Client {client_id} Message")
                # await websocket.recv()  # Commented out to keep the connection open
            print(f"Client {client_id} completed.")

    tasks = [simulate_client(i) for i in range(num_clients)]
    await asyncio.gather(*tasks)
    await asyncio.sleep(duration_seconds)  # Hold the connections open for the specified duration

async def main():
    print("Running Latency Measurement:")
    await measure_latency() #this function will give us the information about latency

    print("\nRunning Throughput Measurement please wait:")
    await measure_throughput(10000) # we can increase or decrease this number for testing.

    print("\nRunning Resource Utilization Measurement please wait:") #it will give us the machine resource utilization information
    resource_task = asyncio.create_task(measure_resource_utilization())
    await asyncio.sleep(15)
    resource_task.cancel()

    print("\nRunning Scalability Test please wait:")
    await measure_scalability(num_clients=20, messages_per_client=50, duration_seconds=20)# We test the server scalability here with connecting with more clients at a time.
    print("\nScalability Test Completed. Testing is over!")

if __name__ == "__main__":
    asyncio.run(main())

"""
**Hardware Details:**
- **CPU:** Intel(R) Core(TM) i7-10875H CPU @ 2.30GHz   2.30 GHz
- **RAM:** 16GB
- **Operating System:** Windows 10
- **Number of Cores Utilized:** 1 (in adherence to the case study instructions)
- **Number of Cores 8
- **Number of Threads Utilized:** 1 (in adherence to the case study instructions)
- **I executed the code within a Conda environment, utilizing only the necessary libraries, and using Python 3.8.
"""