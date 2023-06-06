from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from contextlib import ExitStack
from spherov2.types import Color
import asyncio


def set_matrix(bot, color):
    bot.set_matrix_fill(
        2, 0, 6, 6, Color(r=int(color[0]), g=int(color[1]), b=int(color[2]))
    )


def connect_to_sphero(stack, toy, index):
    attempts = 0
    while attempts < 3:
        print(
            "Connecting to sphero {index}, attempt {attempt}".format(
                index=index, attempt=attempts + 1
            )
        )
        try:
            bots.append(stack.enter_context(SpheroEduAPI(toy)))
            print("Connected to sphero {index}".format(index=index))
            return
        except:
            print(
                "Somethine went wrong with sphero {index}, retyring".format(index=index)
            )
            attempts += 1


async def main():
    pass
    with ExitStack() as stack:
        await asyncio.gather(
            *[asyncio.to_thread(connect_to_sphero, stack, toys[i], i) for i in range(7)]
        )
        while True:
            color = input("Color?")
            color = color.split(",")
            await asyncio.gather(
                *[asyncio.to_thread(set_matrix, bot, color) for bot in bots]
            )


toys = scanner.find_toys()
bots = []
print(toys)

asyncio.run(main())
