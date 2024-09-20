import asyncio


async def fetch_data():
    print("Start fetching data...")
    await asyncio.sleep(2)
    print("Data fetched")
    return {"data": "example"}


async def main():
    print("Main started")
    data = await fetch_data()
    print(f"Result: {data}")


asyncio.run(main())
