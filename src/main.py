import os
import global_data
import configparser
import pathlib
import requestRoutes.announcePost
import requestRoutes.announceGet
import websocket.socketServer
import websocket.socketClient

os.chdir(pathlib.Path(__file__).parent.resolve())

if os.path.exists("./output/OutputFile"):
    overwriteDecision = input("Output file exists. Overwrite? Y/N\n> ")
    if overwriteDecision == "Y":
        os.unlink("./output/OutputFile")
    else:
        exit(0)

if os.path.exists("./config/main.ini"):
    print(
        "Config loaded. If you want to switch your server, please edit the main.ini in the config project directory."
    )

    config = configparser.ConfigParser()
    config.read("./config/main.ini")
else:
    config = configparser.ConfigParser()
    config["SERVER"] = {"url": ""}
    config["SERVER"]["url"] = input("Please enter the Server URL\n> ")

    print(
        "Config saved. If you want to switch your server, please edit the main.ini in the config project directory."
    )

    with open("./config/main.ini", "w") as configfile:
        config.write(configfile)

clientType = input("Do you want to act as sender (1) or as reciever (2)\n> ")

if clientType == "1":
    clientData = requestRoutes.announcePost.announceClient(config)

    global_data.client_id = clientData["id"]
    global_data.client_secret = clientData["token"]

    print(
        "Client data retrieved. Please hand your ID and token to your partner. Its valid for 5 minutes.\nID: "
        + clientData["id"]
        + "\nToken: "
        + clientData["token"]
    )
    websocket.socketServer.Server()
else:
    partnerID = input("Please enter the Client ID of your partner\n> ")

    clientData = requestRoutes.announceGet.getAnnouncedClient(config, partnerID)

    if clientData[0] != None:
        websocket.socketClient.main(clientData[0]["ip"], partnerID)
    else:
        print("Wrong ID!")
