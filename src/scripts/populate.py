import random
import asyncio
from datetime import datetime
from asyncio import TaskGroup

from httpx import AsyncClient

SOURCE_COUNT = 30
EVENT_COUNT = 10
COUNTER_LIMIT = 5

ENDPOINT = "http://localhost:8000/api/v1/receiver/"
token = "this.some.token"


async def generate_object():
    fields = ["A", "B", "C", "D", "E", "F"]
    timestamp = random.randint(1683465739, int(datetime.now().timestamp()))
    num_params = random.randint(1, len(fields))

    params = {}
    for _ in range(num_params):
        param_key = random.choice(fields)
        params[param_key] = random.randint(1, 9)

    data = {'timestamp': timestamp}
    data.update(params)
    return data


async def source(tg: TaskGroup, client: AsyncClient):
    for _ in range(EVENT_COUNT):
        data = await tg.create_task(generate_object())
        resp = await client.post(
            ENDPOINT,
            json=data,
            headers={"Authorization": "bearer " + token}
        )
        print(f"Status: {resp.status_code},  Sent data: {data}")


async def main():
    async with TaskGroup() as tg, AsyncClient() as client:
        counter = 0

        while True:
            for _ in range(SOURCE_COUNT):
                tg.create_task(source(tg, client))

            counter += 1

            if counter == COUNTER_LIMIT:
                break

            print("-----")
            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())