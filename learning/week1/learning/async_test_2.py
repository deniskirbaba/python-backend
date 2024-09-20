import asyncio
import time

async def fetch_url(url):
    print(f"Fetching {url}...")
    await asyncio.sleep(2)  # Simulating an I/O-bound task (e.g., network request)
    print(f"Finished fetching {url}")
    return url

async def main():
    urls = ['http://example.com', 'http://example.org', 'http://example.net']
    
    # Schedule all tasks to run concurrently
    tasks = [fetch_url(url) for url in urls]
    
    start = time.time()
    results = await asyncio.gather(*tasks)  # Run tasks concurrently
    print(f"All URLs fetched in {time.time() - start} seconds")

# Run the asynchronous main function
asyncio.run(main())
