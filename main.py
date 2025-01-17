import asyncio

from berrycorepy.client.client import Client
from berrycorepy.types.User import User

client = Client("testToken")


async def main() -> None:

    user: User = await client.get_me()


if __name__ == "__main__":
    asyncio.run(main())