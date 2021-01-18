from wetransfer import main as wtget
import requests
import sys
import re
import os
import time
from pyunpack import Archive 
from os.path import join

ALL_PATCH_URLS = [
            {
                "game": "Sakura Dungeon",
                "URL": "https://we.tl/EGJuqaTyOd"
            },
            {
                "game": "Sakura Fantasy",
                "URL": "https://we.tl/GXMoHoWKRT"
            },
            {
                "game": "Sakura Space",
                "URL": "https://we.tl/rzw8uYu0rS"
            },
            {
                "game": "Sakura Swim Club",
                "URL": "https://we.tl/zWlFopavSh"
            },
            {
                "game": "Sakura Nova",
                "URL": "https://we.tl/T5zouesQBi"
            },
            {
                "game": "Sakura Agent",
                "URL": "https://wingedcloud.wetransfer.com/downloads/502682c02648ba2bcee9306b45ba237c20170127114431/89dc8a"
            },
            {
                "game": "Sakura Magical Girls",
                "URL": "https://we.tl/2mzl9lMihN"
            },
            {
                "game": "Sakura Cupid",
                "URL": "https://wingedcloud.wetransfer.com/downloads/f623887cf50ff53460826f30bae7991920180212164017/d21d1e"
            },
            {
                "game": "Sakura Sadist",
                "URL": "https://we.tl/S31ZAAwfuO"
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
]

def main(argv):
    if len(argv) == 0:
        print("Use the sakura-patcher like this: python sakura_patcher.py [Steam Libary Path here]\n For me it's K://")
    
    gameCollectionDir = join(argv[0], "Steam/steamapps/common/")
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
                print("Patch availabel for {0}".format(game))

    for patch in neededPatchFiles:
        print("Downloading patch for {0}".format(patch["game"]))
        wtget(patch["URL"])
        print("Download finished for {0}".format(patch["game"]))
        fileDest = join(gameCollectionDir, patch["game"],"game/")
        cwdContent = os.listdir(os.getcwd())
        cwd = os.getcwd()
        for file in cwdContent:
            
            if patch["game"] == "Sakura Swim Club":
                print("Moving file to dir: {0}".format(fileDest))
                f_cont = []
                with open(join(fileDest, "archive.rpa"), "rb") as f:
                    f_cont = f.readlines()
                with open(join(fileDest, "archive.rpa"), "wb") as f:
                    f.writelines(f_cont)


            if file.endswith(".rpa"):
                print("Moving file to dir: {0}".format(fileDest))
                try:
                    os.remove(join(fileDest, file))
                except:
                    pass
                try:
                    os.rename(file, join(fileDest, file)) 
                except:
                    print("File can't be installed")
                    os.remove(file)              

if __name__ == "__main__":
    main(sys.argv[1:])    