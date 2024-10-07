import asyncio
import random

import httpx

BASE_URL = "http://0.0.0.0:8080"

ENDPOINTS = [
    "/cart",
    "/item",
    "/cart/{cart_id}",
    "/cart/{cart_id}/add/{item_id}",
    "/cart/{cart_id}/remove/{item_id}",
    "/item/{item_id}",
    "/cart?offset=0&limit=10",
    "/item?offset=0&limit=10",
]


def prepare_endpoint(endpoint, cart_id=None, item_id=None):
    if "{cart_id}" in endpoint:
        cart_id = cart_id or random.randint(1, 100)
        endpoint = endpoint.replace("{cart_id}", str(cart_id))
    if "{item_id}" in endpoint:
        item_id = item_id or random.randint(1, 100)
        endpoint = endpoint.replace("{item_id}", str(item_id))
    return endpoint


async def send_request(client, endpoint):
    try:
        url = f"{BASE_URL}{endpoint}"
        method = random.choice(["get", "post", "patch", "put", "delete"])
        if method in ["post", "patch", "put"]:
            json_body = {
                "name": f"Random Item {random.randint(1, 100)}",
                "price": random.uniform(10, 100),
            }
            response = await client.request(method, url, json=json_body)
        else:
            response = await client.request(method, url)

        print(
            f"Request to {url} with method {method.upper()} returned status {response.status_code}"
        )
    except Exception as e:
        print(f"Error sending request to {url}: {e}")


async def ddoser(rps, client):
    interval = 1.0 / rps
    while True:
        endpoint = prepare_endpoint(random.choice(ENDPOINTS))
        asyncio.create_task(send_request(client, endpoint))
        await asyncio.sleep(interval)


async def main():
    async with httpx.AsyncClient() as client:
        rps_rates = [1, 5, 10, 50, 100]

        tasks = []
        for rps in rps_rates:
            print(f"Starting attack at {rps} RPS...")
            tasks.append(asyncio.create_task(ddoser(rps, client)))

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
