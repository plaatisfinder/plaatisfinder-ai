import asyncio

from plaatisfinder.telegram.notifier import send_message


async def main():
    print("🚐 PlaatisFinder startar...")

    await send_message("🎉 Första meddelandet från PlaatisFinder!")


if __name__ == "__main__":
    asyncio.run(main())