from wetransfer import main as wtget
import requests
import sys
import re
import os
import time
from pyunpack import Archive 
from os.path import join
from zipfile import ZipFile

ALL_PATCH_URLS = [
            {
                "game": "Sakura Agent",
                "URL": "https://wingedcloud.wetransfer.com/downloads/502682c02648ba2bcee9306b45ba237c20170127114431/89dc8a"
            },
            {
                "game": "Sakura Cupid",
                "URL": "https://wingedcloud.wetransfer.com/downloads/f623887cf50ff53460826f30bae7991920180212164017/d21d1e"
            },
            {
                "game": "Sakura Dungeon",
                "URL": "https://we.tl/EGJuqaTyOd"
            },
            {
                "game": "Sakura Fantasy",
                "URL": "https://we.tl/GXMoHoWKRT"
            },
            {
                "game": "Sakura Fox Adventure",
                "URL": "https://wingedcloud.wetransfer.com/downloads/f1c49f046bd16d7d70a8374f50155a5020191008143738/01b9cf"
            },
            {
                "game": "Sakura Gamer",
                "URL": "https://we.tl/oQHcuoKcc1"
            },
            {
                "game": "Sakura Gamer 2",
                "URL": "https://we.tl/t-gT5n1FEfpC"
            },
            {
                "game": "Sakura Knight",
                "URL": "https://we.tl/t-RJhUv8UVnr"
            },
            {
                "game": "Sakura Knight 2",
                "URL": "https://we.tl/t-0CVFnxH11k"
            },
            {
                "game": "Sakura Knight 3",
                "URL": "https://we.tl/t-lBzY2OU47A"
            },
            {
                "game": "Sakura Magical Girls",
                "URL": "https://we.tl/2mzl9lMihN"
            },
            {
                "game": "Sakura MMO",
                "URL": "https://wingedcloud.wetransfer.com/downloads/bf8463cc8dab12b3a8fc2083a21d761a20181015181223/7c26ed"
            },
            {
                "game": "Sakura MMO 2",
                "URL": "https://we.tl/t-VxxEtpMQPK"
            },
            {
                "game": "Sakura MMO 3",
                "URL": "https://wingedcloud.wetransfer.com/downloads/a3cffdd814a43e59c6d87b970fa1a0af20190605180849/6103c4"
            },
            {
                "game": "Sakura MMO Extra",
                "URL": "https://we.tl/t-LkqNrUSkBX"
            },
            {
                "game": "Sakura Nova",
                "URL": "https://we.tl/T5zouesQBi"
            },
            {
                "game": "Sakura Sadist",
                "URL": "https://we.tl/S31ZAAwfuO"
            },
            {
                "game": "Sakura Space",
                "URL": "https://we.tl/rzw8uYu0rS"
            },
            {
                "game": "Sakura Succubus",
                "URL": "https://wingedcloud.wetransfer.com/downloads/717fedf8dcc50d0e1611a170a2971ce120200310192553/c249a2"
            },
            {
                "game": "Sakura Succubus 2",
                "URL": "https://we.tl/t-jhWiowJzNN"
            },
            {
                "game": "Sakura Succubus 3",
                "URL": "https://we.tl/t-EsZuGK9yd9"
            },
            {
                "game": "Sakura Swim Club", 
                "URL": "" # https://we.tl/zWlFopavSh
            },
]

def main(argv):
    if len(argv) == 0:
        print("Use the sakura-patcher like this: python sakura_patcher.py [Steam Libary Path here]\n For me it's K://")
    
    gameCollectionDir = join(argv[0], "Steam//steamapps//common//")
    allGames = os.listdir(gameCollectionDir)
    sakuraGames = []
    for game in allGames:
        if game.startswith("Sakura"):
            sakuraGames.append(game)

    neededPatchFiles = []
    for patch in ALL_PATCH_URLS:
        for game in sakuraGames:
            if patch["game"] == game:
                neededPatchFiles.append(patch)
                if not os.path.isdir(join(os.getcwd(), patch["game"])):
                    os.mkdir(join(os.getcwd(), patch["game"]))
                print("Patch availabel for {0}".format(game))

    for idx, patch in enumerate(neededPatchFiles):
        print("---------{0}.{1}---------".format(idx + 1, patch["game"]))
        print("Downloading patch for {0}".format(patch["game"]))
        
        cwd = os.getcwd()
        if patch["URL"] != "":
            wtget(patch["URL"])
            for file in os.listdir(cwd):
                if file.endswith(".zip"):
                    with ZipFile(file, 'r') as zipObj:
                        zipObj.extractall()
                    os.remove(file)


            for file in os.listdir(cwd):
                if file.endswith(".rpa"):
                    os.rename(file, join(cwd, patch["game"], file))


        print("Download finished for {0}".format(patch["game"]))
        fileDest = join(gameCollectionDir, patch["game"],"game/")
        
        for file in os.listdir(join(cwd, patch["game"])):
            print("Moving file to dir: {0}".format(fileDest))

            destFile = join(fileDest, file)

            if os.path.isfile(destFile) and not os.path.isfile(destFile + "-copy"):
                os.rename(destFile, destFile + "-copy") 

            f_cont = []
            with open(join(cwd, patch["game"], file), "rb") as f:
                f_cont = f.readlines()
            with open(join(fileDest, file), "wb+") as f:
                f.writelines(f_cont)
            

            if os.path.isfile(destFile):
                print("Moving file to dir done!")
            else:
                print("Moving file to dir ERROR!")

        # The download link for SSC is a .rar file and requiers additional software to unpack
        # thats why this is the only static binary in this repository
        cleanUp = True
        if cleanUp and patch["game"] != "Sakura Swim Club":
            print("Removing temp .rpa file(s) for game {0}".format(patch["game"]))
            tempGameDir = join(cwd, patch["game"])
            try:
                for file in os.listdir(tempGameDir):
                    os.remove(join(tempGameDir,file))

                print("File(s) removed successfully")
            except:
                print("File(s) could not be removed automatically")

            print("Removing temp dir for game {0}".format(patch["game"]))
            try:
                os.rmdir(tempGameDir)
                print("Directory removed successfully")
            except:
                print("Directory could not be removed automatically")

        
            
             

if __name__ == "__main__":
    main(sys.argv[1:])    