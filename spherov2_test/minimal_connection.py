import asyncio
import bleak

handshake = [('00020005-574f-4f20-5370-6865726f2121', bytearray(b'usetheforce...band'))]
response_uuid = '00010002-574f-4f20-5370-6865726f2121'
send_uuid = '00010002-574f-4f20-5370-6865726f2121'

wake_command = b'\x8d\n\x13\r\x00\xd5\xd8'

async def main():
    # Find devices

    bots = []

    for index, sphero in enumerate(sphero_names):

        adapter = "hci1" if index % 2 else "hci0"

        device = await bleak.BleakScanner.find_device_by_name(sphero, 10.0, adapter=adapter)

        bot = bleak.BleakClient(device, timeout=5.0)
        try:
            print("Connecting to bot: {name} using {adapter}".format(name=device.name, adapter=adapter))
            await bot.connect()
            print("Connected to bot: {name}".format(name=device.name))
            bots.append(bot)
            # Perform handshake
            for uuid, data in handshake:
                await bot.write_gatt_char(uuid, data, True)
            await bot.start_notify(response_uuid, lambda x, y: None)
            print("Performed handshake")
            # Wake up the device
            await bot.write_gatt_char(send_uuid, wake_command, True)
        except Exception as e:
            print("Exception!")
            print(e)
        
    wait = input("Disconnect?")

    for bot in bots:
        await bot.disconnect()

sphero_names = ["SB-1B35", "SB-2175", "SB-3026", "SB-618E", "SB-6B58", "SB-9938", "SB-BFD4", "SB-C1D2", "SB-CEFA", "SB-DF1D", "SB-F465", "SB-F479", "SB-F885", "SB-FCB2"]

asyncio.run(main())