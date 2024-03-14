from wetransfer import main as wtget
import sys
import os
from os.path import join
from zipfile import ZipFile
from hashlib import md5
from patoolib import extract_archive
from shutil import rmtree
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

## md5sum assets.rpa | tr '[:lower:]' '[:upper:]'
ALL_PATCHES = [
            {
                "game": "Leveling Up Girls in Another World",
                "URL": "https://wingedcloud.wetransfer.com/downloads/b1eb59fad8accec6c4027ae57423d35a20230428210948/279548",
                "hashes": {
                    "AssetBundlesLeveling": "1E1D9BED3B769D44E50E929322BA6970",
                    "AssetBundlesLeveling.manifest": "629DA33BC0E78D682A49E47073351D2F",
                    "mod": "0142E1A71FFDCC3713DB70311A0E95FF",
                    "mod.manifest": "F902B493BA99418EE1686DCAC7D785AF"
                }
            },
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
                "game": "Sakura Alien 2",
                "URL": "https://we.tl/t-gIwaJT7aEB",
                "hashes": {"assets.rpa": "38853D179E5DB4D9C4BB458D4651756F"}
            },
            {
                "game": "Sakura Bunny Girls",
                "URL": "https://we.tl/t-gVOO5RmRlX",
                "hashes": {"assets.rpa": "936C3720B408F87F2062C2BCBEF4A64B"}
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
                "URL": "https://we.tl/t-N7RgVi1FvG",
                "hashes": {"assets.rpa": "093B2BFB67DD45C4C84D6F97E2D01630"}
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
                "game": "Sakura Gym Girls",
                "URL": "https://we.tl/t-3iM3F94CFT",
                "hashes": {"assets.rpa": "0A61430125924A2216C703A1902A7C1E"}
            },
            {
                "game": "Sakura Gym Girls Prologue",
                "URL": "https://we.tl/t-JD2E6Q9L9z",
                "hashes": {"assets.rpa": "18EA347BFABED9232314E3B619AE0B78"}
            },
            {
                "game": "Sakura Isekai Adventure",
                "URL": "https://wingedcloud.wetransfer.com/downloads/bcc16b1417bcc27e381135a170aed6ab20240224185018/364813",
                "hashes": {"assets.rpa": "3F6A703B3B6DE2B26565D231649608A1"}
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
                "game": "Sakura Melody",
                "URL": "https://we.tl/t-wNzkLxOLyD",
                "hashes": {
                    "AssetBundlesMelody": "EF35A60467AB55DD852FDBBF46B29917",
                    "AssetBundlesMelody.manifest": "D9841CADD084AFF8DEECEADA2EF673FB",
                    "modsakuramelody": "49E617F424C0DD752ECB4E9D29F9E3DA",
                    "modsakuramelody.manifest": "A889AC9850E66DC4CCE7961C7517BFF9"
                }
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
                "game": "Sakura Succubus 5",
                "URL": "https://we.tl/t-ASDXsLvbU6",
                "hashes": {"assets.rpa": "4B9DC63A5E71977DEDD61921273D9A67"}
            },
            {
                "game": "Sakura Succubus 6",
                "URL": "https://wingedcloud.wetransfer.com/downloads/523624e1b6a45336e83c5a28a7ad7b0b20220705144353/cb84fb",
                "hashes": {"assets.rpa": "B511833EFA3C93A4763A353D20491799"}
            },
            {
                "game": "Sakura Succubus 7",
                "URL": "https://wingedcloud.wetransfer.com/downloads/416fc0128979213543ce6d48badca73620230306163155/f95f07",
                "hashes": {"assets.rpa": "DBAB0DA060D40CB06ECBA711175449CA"}
            },
            {
                "game": "Sakura Succubus 8",
                "URL": "https://we.tl/t-HBVLOUeYTb",
                "hashes": {"assets.rpa": "44E11B371351D5024AC02BE7A128A6F8"}
            },
            {
                "game": "Sakura Swim Club", 
                "URL": "https://we.tl/zWlFopavSh", 
                "hashes": {"archive.rpa": "C260A1AFA2E3422D84C2A6320A5DF070"}
            },
            {
                "game": "Would you like to run an idol café", 
                "URL": "https://we.tl/t-JkNwJ0Bj0M",
                "hashes": {"assets.rpa": "8234BCD2BB49989F14D1CE35E9CB1583"}
            },
            {
                "game": "Would you like to run an idol café 2", 
                "URL": "https://we.tl/t-Prc7eoSi4S",
                "hashes": {"assets.rpa": "35347CD8CEC81E2A424242CAAC00B0DB"}
            },
            {
                "game": "Would you like to run an idol café 3", 
                "URL": "https://wingedcloud.wetransfer.com/downloads/f8f92d4845de4fd98e45caa19244622420220509155624/685a36",
                "hashes": {"assets.rpa": "E53F18CA02E18C1D30F346A3AE884C5E"}
            },
]

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
        self.filesBefore = []
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
            if game.startswith("Sakura") or game.startswith("Would you like to run an idol café"):
                sakuraGames.append(game)

        self.filesBefore = os.listdir(os.getcwd())
        self.neededPatchFiles = []
        for patch in ALL_PATCHES:
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
                        
                        md5Hash = md5()
                        with open(hashFile, "rb") as f:
                            md5Hash.update(f.read())
                        if v != md5Hash.hexdigest().upper():
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
                    elif file.endswith(".rar"):
                        extract_archive(file, outdir=cwd, interactive=False)


                for root, directory, files in os.walk(cwd):
                    for file in files:
                        if any(file in k for k in patch["hashes"].keys()):
                            try:
                                os.rename(join(root, file), join(cwd, patch["game"], file))
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
        if len(self.filesBefore) < 1:
            return

        for d in os.listdir(os.getcwd()):
            if any(d in f for f in self.filesBefore):
                continue
            
            try:
                os.remove(d)
                print("File {} removed successfully".format(d))
            except:
                pass
                #print("File(s) could not be removed automatically")

            #print("Removing temp dir for game {0}".format(patch["game"]))
            try:
                rmtree(join(os.getcwd(), d), ignore_errors = True)
                print("Directory {} removed successfully".format(d))
            except:
                pass
                #print("Directory could not be removed automatically")


if __name__ == "__main__":
    #main(sys.argv[1:])
    app = QApplication(sys.argv)

    patcher = Patcher()
    patcher.show()

    sys.exit(app.exec_())
