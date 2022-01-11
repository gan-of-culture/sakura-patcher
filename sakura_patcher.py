from wetransfer import main as wtget
import requests
import sys
import re
import os
import time
from os.path import join
from zipfile import ZipFile
from hashlib import md5
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

## md5sum assets.rpa | tr '[:lower:]' '[:upper:]'
ALL_PATCH_URLS = [
            {
                "game": "Sakura Agent",
                "URL": "https://wingedcloud.wetransfer.com/downloads/502682c02648ba2bcee9306b45ba237c20170127114431/89dc8a",
                "hashes": {"archive.rpa": "CEEF65D0B07C1306277663C0CC3FC127"}
            },
            {
                "game": "Sakura Alien",
                "URL": "https://we.tl/t-mGqvYtTTZE",
                "hashes": {"assets.rpa": "94446DE3804E3421CB93E7B66A3B4BD0"}
            },
            {
                "game": "Sakura Cupid",
                "URL": "https://wingedcloud.wetransfer.com/downloads/f623887cf50ff53460826f30bae7991920180212164017/d21d1e",
                "hashes": {"assets.rpa": "1E9F197DC71AE536A92E7C05B689F9E9"}
            },
            {
                "game": "Sakura Dungeon",
                "URL": "https://we.tl/EGJuqaTyOd",
                "hashes": {"patch0x.rpa": "09302BA1B4CD5669EA70BC315D14CE9E"}
            },
            {
                "game": "Sakura Fantasy",
                "URL": "https://we.tl/GXMoHoWKRT",
                "hashes": {"archive.rpa": "CC3CE2B581103DF81C2F29504AE0DC13"}
            },
            {
                "game": "Sakura Forest Girls",
                "URL": "https://wingedcloud.wetransfer.com/downloads/5179f6ba1e1c910fe0efb80403b1b5e320210419152946/d5ba4b",
                "hashes": {"assets.rpa": "2E838AD5BAB2A8C6F481F5D0D218C129"}
            },
            {
                "game": "Sakura Forest Girls 2",
                "URL": "https://we.tl/t-rxVpHynlrU",
                "hashes": {"assets.rpa": "A1DC9AFD2D830621026F2C673ACB30D6"}
            },
            {
                "game": "Sakura Forest Girls 3",
                "URL": "https://we.tl/t-IkVpJyBnkn",
                "hashes": {"assets.rpa": "536747A55ABA1B3256780DFCA1F6C4AC"}
            },
            {
                "game": "Sakura Fox Adventure",
                "URL": "https://wingedcloud.wetransfer.com/downloads/f1c49f046bd16d7d70a8374f50155a5020191008143738/01b9cf",
                "hashes": {"assets.rpa": "C0ED849280955609FB3905AC9A28DC55"}
            },
            {
                "game": "Sakura Gamer",
                "URL": "https://wingedcloud.wetransfer.com/downloads/61997c1379509ff9d2f630a8ec5d5ab420171003121859/085abf",
                "hashes": {
                    "assets.rpa": "7218A1DF1FDA802270B9BB81845E841D",
                    "archive.rpa": "AEE716A9D95CDAEF81069C86B3C2834E"
                }
            },
            {
                "game": "Sakura Gamer 2",
                "URL": "https://we.tl/t-gT5n1FEfpC",
                "hashes": {"assets.rpa": "C02C462A3BA6DF012D9D2F3F71F9F906"}
            },
            {
                "game": "Sakura Knight",
                "URL": "https://we.tl/t-RJhUv8UVnr",
                "hashes": {"assets.rpa": "48512025AAE192240A5E8C9DA3017DC0"}
            },
            {
                "game": "Sakura Knight 2",
                "URL": "https://we.tl/t-0CVFnxH11k",
                "hashes": {"assets.rpa": "044353FF163EC089A4F4C683E80E060D"}
            },
            {
                "game": "Sakura Knight 3",
                "URL": "https://we.tl/t-lBzY2OU47A",
                "hashes": {"assets.rpa": "6A3A7E8FB67A6FAC7051971DCE79E95A"}
            },
            {
                "game": "Sakura Magical Girls",
                "URL": "https://we.tl/2mzl9lMihN",
                "hashes": {"adult.rpa": "DE07120C6A589F3360996F88011FD9AC"}
            },
            {
                "game": "Sakura MMO",
                "URL": "https://wingedcloud.wetransfer.com/downloads/bf8463cc8dab12b3a8fc2083a21d761a20181015181223/7c26ed",
                "hashes": {"assets.rpa": "F7EF0524CC3B466C27BA813CD6EF797E"}
            },
            {
                "game": "Sakura MMO 2",
                "URL": "https://we.tl/t-VxxEtpMQPK",
                "hashes": {"assets.rpa": "AFAFBE6346DD3F43556B47BBBE74F408"}
            },
            {
                "game": "Sakura MMO 3",
                "URL": "https://wingedcloud.wetransfer.com/downloads/a3cffdd814a43e59c6d87b970fa1a0af20190605180849/6103c4",
                "hashes": {"assets.rpa": "3A072446452592FF605DF574535CEF5B"}
            },
            {
                "game": "Sakura MMO Extra",
                "URL": "https://we.tl/t-LkqNrUSkBX",
                "hashes": {"assets.rpa": "FCA9FBB2ACCCEB6959C4B7F7A949994C"}
            },
            {
                "game": "Sakura Nova",
                "URL": "https://we.tl/T5zouesQBi",
                "hashes": {"assets.rpa": "DC7B10CF68C15D4A13E734CED2624C8F"}
            },
            {
                "game": "Sakura Sadist",
                "URL": "https://we.tl/S31ZAAwfuO",
                "hashes": {"assets.rpa": "93A3BA8B4D2DD6F7DE98F4B4C5199F47"}
            },
            {
                "game": "Sakura Space",
                "URL": "https://we.tl/rzw8uYu0rS",
                "hashes": {"archive.rpa": "71FF3F4A052A97CE86FCF042E1EB32F4"}
            },
            {
                "game": "Sakura Succubus",
                "URL": "https://wingedcloud.wetransfer.com/downloads/717fedf8dcc50d0e1611a170a2971ce120200310192553/c249a2",
                "hashes": {"assets.rpa": "5D9F1E0321A4A3BA1564FF0BD4BA29F3"}
            },
            {
                "game": "Sakura Succubus 2",
                "URL": "https://we.tl/t-jhWiowJzNN",
                "hashes": {"assets.rpa": "012EA641EEDCEBCFCF71D10324D85BBF"}
            },
            {
                "game": "Sakura Succubus 3",
                "URL": "https://we.tl/t-EsZuGK9yd9",
                "hashes": {"assets.rpa": "766A8AF11D50AC3482604121229251F8"}
            },
            {
                "game": "Sakura Succubus 4",
                "URL": "https://wingedcloud.wetransfer.com/downloads/6e573c87617607b16d9c3dafb5ce75dc20210301161546/8c6ad5",
                "hashes": {"assets.rpa": "8E184B9B3CFCC1BFF9E6EC98B3DCFC9D"}
            },
            {
                "game": "Sakura Swim Club", 
                "URL": "", # https://we.tl/zWlFopavSh
                "hashes": {"archive.rpa": "56266B40134B76D60876C5AA9419AF0F"}
            },{
                "game": "Would you like to run an idol café?", 
                "URL": "https://we.tl/t-JkNwJ0Bj0M",
                "hashes": {"assets.rpa": "8234BCD2BB49989F14D1CE35E9CB1583"}
            },{
                "game": "Would you like to run an idol café? 2", 
                "URL": "https://we.tl/t-Prc7eoSi4S",
                "hashes": {"assets.rpa": "35347CD8CEC81E2A424242CAAC00B0DB"}
            },
]

STEAM_LIB_PATH_EXT = "Steam//steamapps//common//"

class Patcher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.destroyed.connect(self.cleanUp)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName(u"centralwidget")
        self.patch = QPushButton(self.centralwidget)
        self.patch.setObjectName(u"patch")
        self.patch.setGeometry(QRect(680, 10, 101, 24))
        self.patch.clicked.connect(self.runPatch)
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(610, 40, 171, 23))
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.selectAll = QPushButton(self.centralwidget)
        self.selectAll.setObjectName(u"selectAll")
        self.selectAll.setGeometry(QRect(450, 40, 75, 24))
        self.selectAll.clicked.connect(self.selectAllItems)
        self.deselectAll = QPushButton(self.centralwidget)
        self.deselectAll.setObjectName(u"deselectAll")
        self.deselectAll.setGeometry(QRect(530, 40, 75, 24))
        self.deselectAll.clicked.connect(self.deselectAllItems)
        self.pathToGames = QLineEdit(self.centralwidget)
        self.pathToGames.setObjectName(u"pathToGames")
        self.pathToGames.setGeometry(QRect(10, 10, 441, 22))
        self.pathToGames.textChanged.connect(self.updateItems)
        self.browse = QPushButton(self.centralwidget)
        self.browse.setObjectName(u"browse")
        self.browse.setGeometry(QRect(450, 10, 31, 22))
        self.browse.clicked.connect(self.browseFiles)
        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(10, 80, 771, 471))
        self.listWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.refresh = QPushButton(self.centralwidget)
        self.refresh.setObjectName(u"refresh")
        self.refresh.setGeometry(QRect(10, 40, 75, 24))
        self.refresh.clicked.connect(self.clear)
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName(u"statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()

        QMetaObject.connectSlotsByName(self)

        self.neededPatchFiles = []
    # setupUi

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("Patcher", u"Patcher", None))
        self.patch.setText(QCoreApplication.translate("Patcher", u"Patch selected", None))
        self.selectAll.setText(QCoreApplication.translate("Patcher", u"Select all", None))
        self.deselectAll.setText(QCoreApplication.translate("Patcher", u"Deselect all", None))
        self.refresh.setText(QCoreApplication.translate("Patcher", u"Refresh", None))
        self.pathToGames.setText("")
        self.pathToGames.setPlaceholderText(QCoreApplication.translate("Patcher", u"Path to your sakura games", None))
        self.browse.setText(QCoreApplication.translate("Patcher", u"...", None))
    # retranslateUi

    def browseFiles(self):
        dirName = QFileDialog.getExistingDirectory(self, "Open directory", os.path.abspath("~//Desktop//"))
        self.pathToGames.setText(dirName)

    def updateItems(self):
        self.listWidget.clear()

        allGames = os.listdir(self.pathToGames.text())
        sakuraGames = []
        for game in allGames:
            if game.startswith("Sakura"):
                sakuraGames.append(game)

        self.neededPatchFiles = []
        for patch in ALL_PATCH_URLS:
            for game in sakuraGames:
                if patch["game"] == game:
                    needsPatch = False

                    #check if patch file(s) exists and are the same md5 hash
                    for k, v in patch["hashes"].items():
                        if needsPatch:
                            continue

                        hashFile = join(self.pathToGames.text(), game, "game//", k)
                        #print(hashFile)
                        if not os.path.isfile(hashFile):
                            needsPatch = True
                            continue
                        
                        md5_h = md5()
                        with open(hashFile, "rb") as f:
                            md5_h.update(f.read())
                        if v != md5_h.hexdigest().upper():
                                needsPatch = True
                    
                    if needsPatch:
                        self.neededPatchFiles.append(patch)
                        if not os.path.isdir(join(os.getcwd(), patch["game"])):
                            os.mkdir(join(os.getcwd(), patch["game"]))
                        #print("Patch available for {0}".format(game))

        for p in self.neededPatchFiles:
            item = QListWidgetItem(p["game"])
            self.listWidget.addItem(item)

        self.listWidget.selectAll()

    def selectAllItems(self):
        self.listWidget.selectAll()

    def deselectAllItems(self):
        self.listWidget.clearSelection()

    def clear(self):
        self.progressBar.reset()
        self.updateItems()

    def runPatch(self):
        if len(self.neededPatchFiles) == 0:
            return

        progressPerIter = int(100 / len(self.neededPatchFiles))

        for idx, patch in enumerate(self.neededPatchFiles):
            self.progressBar.setValue(progressPerIter*(idx+1))
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
                        try:
                            os.rename(file, join(cwd, patch["game"], file))
                        except FileExistsError:
                            pass


            print("Download finished for {0}".format(patch["game"]))
            fileDest = join(self.pathToGames.text(), patch["game"],"game/")
            
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

            self.progressBar.setValue(100)
            self.cleanUp()
            self.updateItems()

    def cleanUp(self):
        for d in os.listdir(os.getcwd()):
            # The download link for SSC is a .rar file and requiers additional software to unpack
            # thats why this is the only static binary in this repository
            cleanUp = True
            if cleanUp and d != "Sakura Swim Club" and os.path.isdir(d) and d.startswith("Sakura"):
                try:
                    for file in os.listdir(d):
                        os.remove(join(d,file))

                    print("File(s) removed successfully")
                except:
                    pass
                    #print("File(s) could not be removed automatically")

                #print("Removing temp dir for game {0}".format(patch["game"]))
                try:
                    os.rmdir(d)
                    print("Directory removed successfully")
                except:
                    pass
                    #print("Directory could not be removed automatically")


if __name__ == "__main__":
    #main(sys.argv[1:])
    app = QApplication(sys.argv)

    patcher = Patcher()
    patcher.show()

    sys.exit(app.exec_())
