from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from contextlib import ExitStack
from spherov2.types import Color
import asyncio

# import time

toys = scanner.find_toys()
bots = []

print(toys)


async def set_matrix(bot, color):
    bot.set_matrix_fill(
        2, 0, 6, 6, Color(r=int(color[0]), g=int(color[1]), b=int(color[2]))
    )


async def main():
    with ExitStack() as stack:
        i = 0
        while i < min(len(toys), 10):
            try:
                print(i)
                bots.append(stack.enter_context(SpheroEduAPI(toys[i])))
                i += 1
            except:
                print("Something went wrong with toy:{toy}".format(toy=toys[i]))
        while True:
            color = input("Color?")
            color = color.split(",")
            await asyncio.gather(*[set_matrix(bot, color) for bot in bots])


asyncio.run(main())
# bots = []

# for toy in toys:
#     bots.append(SpheroEduAPI(toy))

# for bot in bots:
#     bot.set_matrix_fill(2, 0, 6, 6, Color(r=0, g=255, b=255)) #Set Matrix Box

# for toy in toys:
#     pass


# if "3026" in toy:
#     print(toy)

# toy = scanner.find_toy()
# with SpheroEduAPI(toy) as api:
#     api.set_matrix_fill(2, 0, 6, 6, Color(r=0, g=255, b=255)) #Set Matrix Box
#     api.set_speed(60)
#     time.sleep(2)
#     api.set_speed(0)
