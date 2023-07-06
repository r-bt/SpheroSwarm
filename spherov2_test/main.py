from spherov2 import scanner
from spherov2.toy.bolt import BOLT
from spherov2.adapter.bleak_adapter import BleakAdapter
from spherov2.sphero_edu import SpheroEduAPI
from contextlib import AsyncExitStack
from spherov2.types import Color
import asyncio
import random

def print_log(data):
    print(data)

async def connect_to_sphero(stack, name, index):
    # Get adapter
    adapter = "hci{index}".format(index=index % 3)
    attempts = 0
    while attempts < 3:
        try:
            print_log("Finding toy...")
            toy = await scanner.find_toy(toy_name=name, bleak_adapter=adapter)
            print_log(
            "Connecting to sphero {name} (#{index}) ({address}), attempt {attempt}, using {adapter}".format(
                name=toy.name, index=index, attempt=attempts + 1, adapter=adapter, address=toy.address
            ))
            bots.append(await stack.enter_async_context(SpheroEduAPI(toy)))
            print_log("Connected to sphero {name} (#{index})".format(name=toy.name, index=index))
            return
        except Exception as e:
            print_log(
                "Something went wrong with sphero {name} (#{index}), retrying".format(name=name, index=index)
            )
            print_log(e)
            attempts += 1

async def set_bots_matrix(color = None):
    if color:
        await asyncio.gather(*(bot.set_matrix_fill(0, 0, 7, 7, Color(r=int(color[0]), g=int(color[1]), b=int(color[2]))) for i, bot in enumerate(bots)))
    else:
        tasks = []
        for bot in bots:
            tasks.append(bot.set_matrix_fill(0, 0, 7, 7, Color(r=int(random.randint(0,255)), g=int(random.randint(0,255)), b=int(random.randint(0,255)))))
        await asyncio.gather(*tasks)

async def all_spin():
    await asyncio.gather(*(bot.spin(1440, 2) for bot in bots))

async def main():
    async with AsyncExitStack() as stack:
        for i in range(min(len(sphero_names), count)):
                await connect_to_sphero(stack, sphero_names[i], i)
        should_quit = False
        await set_bots_matrix()
        quit = input("quit?")
        for bot in bots:
            bot.set_speed(25)
        while True:
            wait = input("Color")
            await all_spin()

        # while not should_quit:
        #     color = input("Color?")
        #     if color == "quit":
        #         should_quit = True  
        #     else:
        #         color = color if color != '' else '255,0,0'
        #         color = color.split(",")
        #         await set_bots_matrix(color)

sphero_names = ["SB-1B35", "SB-F860", "SB-2175", "SB-3026", "SB-618E", "SB-6B58", "SB-9938", "SB-BFD4", "SB-C1D2", "SB-CEFA", "SB-DF1D", "SB-F465", "SB-F479", "SB-F885", "SB-FCB2"]
count = 1

bots = []

print_log("Sphero Swarm! Beginning to connect to {count} spheros".format(count=count))

asyncio.run(main())