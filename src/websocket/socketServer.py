import os
import asyncio
import global_data
from websockets.server import serve
import utliFunctions.progressBar


class Server:
    def __init__(self):
        self.incoming_connections = asyncio.Queue()
        self.is_connected = False

        self.chunk_size = 512 * 512

        self.run()

    async def incoming(self, websocket, path):
        if self.is_connected:
            return

        state = 0

        async for message in websocket:
            if message == global_data.client_id and state == 0:
                self.is_connected = True
                print("Recieved a connection! Authenticating it...")
                state = 1
                await websocket.send("ACKREPLYWITHSECRET")
            elif message == global_data.client_secret and state == 1:
                state = 2
                global_data.filepath = input(
                    "Got valid secret. Please enter the file you want to transfer\n> "
                )
                filestat = os.stat(global_data.filepath)
                global_data.total_file_size = filestat.st_size
                await websocket.send(
                    "ACKFILESTAT|"
                    + str(global_data.filepath)
                    + "|"
                    + str(global_data.total_file_size / (1024 * 1024))
                )
            elif message == "ACKSTARTTRANSFER" and state == 2:
                with open(global_data.filepath, "rb") as f:
                    while chunk := f.read(self.chunk_size):
                        await websocket.send(chunk)
                        global_data.total_bytes_sent += len(chunk)
                        utliFunctions.progressBar.print_progress_bar(
                            global_data.total_bytes_sent, global_data.total_file_size
                        )
                print("\nFile transfer completed!")
                await websocket.close()
            else:
                print("Invalid connection request. Closing connection")
                self.is_connected = False
                await websocket.close()
                return

    async def websocket_server(self):
        async with serve(self.incoming, None, 8765):
            while True:
                if self.is_connected:
                    await asyncio.sleep(1)
                else:
                    await asyncio.sleep(5 * 60)
                    if not self.is_connected:
                        break

    async def main(self):
        print(
            "Websocket server started. Listening for connections for the next 5 Minutes..."
        )
        await self.websocket_server()

    def run(self):
        asyncio.run(self.main())
