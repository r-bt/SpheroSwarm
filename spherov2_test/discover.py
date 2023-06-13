import asyncio
from bleak import BleakScanner, BleakClient
import pdb
from contextlib import ExitStack

notify_uuid = "0000{0:x}-0000-1000-8000-00805f9b34fb".format(0xFFE1)

def callback(characteristic, data):
    print(characteristic, data)

async def main():
    print("scanning for 5 seconds, please wait...")

    devices = await BleakScanner.discover(adapter="hci1")

    ret = []

    for device in devices:
        if (device.name.startswith("SB")):
            ret.append(device)

    print(len(ret))        

    clients = []

    for bot in ret[:1]:
        print(bot)
        client = BleakClient(bot, adapter="hci1")
        await client.connect()
        print("Connected!")
        clients.append(client)

    wait = input("Disconnect?")

    print("Disconnecting")

    for client in clients:
        await client.disconnect()

    print("Disconnected!")

if __name__ == "__main__":
    asyncio.run(main())
