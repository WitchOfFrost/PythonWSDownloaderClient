from websockets.sync.client import connect
import utliFunctions.progressBar
import global_data


def main(ip, id):
    awaitingbinary = False

    with connect("ws://" + ip + ":8765") as websocket:
        websocket.send(id)
        while True:
            try:
                message = websocket.recv()

                if isinstance(message, str):
                    message = message.split("|")

                    if message[0] == "ACKREPLYWITHSECRET":
                        secret = input("Enter your Partners secret\n> ")

                        websocket.send(secret)

                        print("Awaiting filedata...")
                    elif message[0] == "ACKFILESTAT":
                        global_data.total_file_size = float(message[2]) * 1024 * 1024
                        filestatresponse = input(
                            "The following file will be transferred:\nHostPath: "
                            + message[1]
                            + "\nSize: "
                            + message[2]
                            + " MB\nPlease confim: yes (1) / no (2)\n> "
                        )

                        if filestatresponse == "1":
                            awaitingbinary = True
                            websocket.send("ACKSTARTTRANSFER")
                        else:
                            websocket.close()
                elif awaitingbinary and isinstance(message, bytes):
                    with open("./output/OutputFile", "ab") as bfile:
                        bfile.write(message)
                        global_data.total_bytes_sent += len(message)
                        utliFunctions.progressBar.print_progress_bar(
                            global_data.total_bytes_sent, global_data.total_file_size
                        )
                else:
                    websocket.close()
            except Exception as e:
                print(f"Connection closed: {e}")
                break
