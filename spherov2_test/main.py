from spherov2 import scanner
from spherov2.toy.bolt import BOLT
from spherov2.adapter.bleak_adapter import BleakAdapter
from spherov2.sphero_edu import SpheroEduAPI
from contextlib import AsyncExitStack
from spherov2.types import Color
# from bleak import BleakScanner
import asyncio
import pdb
import datetime

async def connect_to_sphero(stack, name, index):
    # Get adapter
    adapter = "hci{index}".format(index=index%3)
    # Find the toy
    try:
        toy = await scanner.find_toy(toy_name=name, bleak_adapter=adapter)
    except Exception as e:
        print(e)
        return
    # Connect to the toy
    attempts = 0
    while attempts < 3:
        print(
            "Connecting to sphero {name} (#{index}), attempt {attempt}, using {adapter}".format(
                name=toy.name, index=index, attempt=attempts + 1, adapter=adapter
            )
        )
        try:
            bots.append(await stack.enter_async_context(SpheroEduAPI(toy)))
            print("Connected to sphero {name} (#{index})".format(name=toy.name, index=index))
            return
        except Exception as e:
            print(
                "Something went wrong with sphero {name} (#{index}), retrying".format(name=toy.name, index=index)
            )
            print(e)
            attempts += 1

async def set_bots_matrix(color):
    print(datetime.datetime.now())
    background_tasks = set()
    async with asyncio.TaskGroup() as tg:
        for bot in bots:
            task = tg.create_task(bot.set_matrix_fill(2, 0, 6, 6, Color(r=int(color[0]), g=int(color[1]), b=int(color[2]))))
            background_tasks.add(task)
            task.add_done_callback(background_tasks.discard)
    print(datetime.datetime.now())


async def main():
    async with AsyncExitStack() as stack:
        for i in range(min(len(sphero_names), 15)):
                await connect_to_sphero(stack, sphero_names[i], i)
        while True:
            color = input("Color?")
            color = color.split(",")
            await set_bots_matrix(color)

sphero_names = ["SB-1B35", "SB-2175", "SB-3026", "SB-618E", "SB-6B58", "SB-9938", "SB-BFD4", "SB-C1D2", "SB-CEFA", "SB-DF1D", "SB-F465", "SB-F479", "SB-F885", "SB-FCB2"]

print("Sphero Swarm! Beginning to connect to {count} spheros".format(count=len(sphero_names)))

# toys = scanner.find_toys()
bots = []
# print(sorted(toys, key=lambda x: x.name))
# if len(toys) != 14:
    # print("Spheros missing!")
# else:

# main()

asyncio.run(main())