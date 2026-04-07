import sys
import os
import re
import json
import unicodedata
import zipfile

from hashlib import md5
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QRunnable, QThreadPool, pyqtSignal, QObject
from PyQt5.QtGui import QColor

from wetransfer import main as wtget

# ================================
# PORTABLE PATHS
# ================================
BASE_DIR = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
CACHE_FILE = os.path.join(BASE_DIR, "patch_cache.json")
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

# ================================
# PATCH LIST
# ================================
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
                "game": "Sakura Alien 3",
                "URL": "https://wingedcloud.wetransfer.com/downloads/306736bce2e799af847546261ebc088820241007144627/1f6da4?t_exp=1759848387&t_lsid=5b26b149-6d26-4dc0-b654-108e536db6a5&t_rid=YXV0aDB8VHJhbnNmZXJ8b2N4eTdzMDl3M2k=&t_s=download_link&t_ts=1728312387",
                "hashes": {"assets.rpa": "7F4D8D3328E86121F9522393DC0DE1E6"}
            },            
            {
                "game": "Sakura Bunny Girls",
                "URL": "https://we.tl/t-gVOO5RmRlX",
                "hashes": {"assets.rpa": "936C3720B408F87F2062C2BCBEF4A64B"}
            },
            {
                "game": "Sakura Bunny Girls 2",
                "URL": "https://we.tl/t-TWKYUBJYvw",
                "hashes": {"assets.rpa": "1474CD2168433EF1AE6A7ACA37D8F44D"}
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
                "game": "Sakura Isekai Adventure 2",
                "URL": "https://wingedcloud.wetransfer.com/downloads/a98fc831d839d4541930aa67662a096720240517185313/b6beb0",
                "hashes": {"assets.rpa": "1378E37AFB6CFDBB4CE686252C1D0421"}
            },
            {
                "game": "Sakura Isekai Adventure 3",
                "URL": "https://wingedcloud.wetransfer.com/downloads/fbdf06f6557d1203c329681a4e0b700420241119210735/a5f237",
                "hashes": {"assets.rpa": "6C0E5CFB1F799CDDB5E81B1000BC77E7"}
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
                "game": "Sakura Succubus 9",
                "URL": "https://we.tl/t-jAcUoCbmxS",
                "hashes": {"assets.rpa": "DFE9E3B8C430964E84DCDA5CDA7242E7"}
            },            
            {
                "game": "Sakura Succubus 10",
                "URL": "https://we.tl/t-ZT4KQL3eU6",
                "hashes": {"assets.rpa": "7DDAEF2FE22CB2D8B95C39439D73250F"}
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

# ================================
# UTILS
# ================================
def normalize_name(name):
    name = name.lower()
    name = unicodedata.normalize('NFKD', name)
    name = name.encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'[^a-z0-9]', '', name)

def build_map(games):
    return {normalize_name(g): g for g in games}

def find_match(name, game_map):
    n = normalize_name(name)
    for k, v in game_map.items():
        if n in k:
            return v
    return None

# ================================
# CACHE
# ================================
def load_json(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# ================================
# STEAM DETECTION
# ================================
def get_steam_libraries():
    libraries = []

    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        drive = f"{letter}:\\"

        paths_to_check = [
            os.path.join(drive, "Program Files (x86)", "Steam", "steamapps", "common"),
            os.path.join(drive, "SteamLibrary", "steamapps", "common")
        ]

        for path in paths_to_check:
            if os.path.isdir(path):
                libraries.append(path)

    return libraries

# ================================
# THREADING
# ================================
class WorkerSignals(QObject):
    progress = pyqtSignal(str, int)
    done = pyqtSignal(str)
    error = pyqtSignal(str)

class PatchWorker(QRunnable):
    def __init__(self, patch, game_path):
        super().__init__()
        self.patch = patch
        self.game_path = game_path
        self.signals = WorkerSignals()

    def run(self):
        try:
            name = self.patch["game"]

            self.signals.progress.emit(name, 0)

            # Download
            wtget(self.patch["URL"])

            # Extract
            for file in os.listdir(os.getcwd()):
                if file.endswith(".zip"):
                    with zipfile.ZipFile(file, 'r') as z:
                        z.extractall(self.game_path)
                    os.remove(file)

            self.signals.progress.emit(name, 100)
            self.signals.done.emit(name)

        except Exception as e:
            self.signals.error.emit(str(e))

# ================================
# MAIN UI
# ================================
class SakuraPatcher(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(300, 200, 700, 750)

        self.cache = load_json(CACHE_FILE)
        self.config = load_json(CONFIG_FILE)

        self.pool = QThreadPool()

        layout = QVBoxLayout()

        # Path
        self.pathBox = QLineEdit()
        layout.addWidget(self.pathBox)

        browse = QPushButton("Browse")
        browse.clicked.connect(self.browse)
        layout.addWidget(browse)

        auto = QPushButton("Auto Detect Steam")
        auto.clicked.connect(self.auto_detect)
        layout.addWidget(auto)

        # Search
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search...")
        self.search.textChanged.connect(self.filter)
        layout.addWidget(self.search)

        # List
        self.listWidget = QListWidget()
        self.listWidget.itemClicked.connect(self.toggle)
        layout.addWidget(self.listWidget)

        # Progress
        self.progress = QProgressBar()
        layout.addWidget(self.progress)

        # Buttons
        btn1 = QPushButton("Patch Selected")
        btn1.clicked.connect(self.patch_selected)
        layout.addWidget(btn1)

        btn2 = QPushButton("Patch All Unpatched")
        btn2.clicked.connect(self.patch_all)
        layout.addWidget(btn2)

        self.status = QLabel("")
        layout.addWidget(self.status)

        self.setLayout(layout)

        # Load last path
        if "last_path" in self.config:
            self.pathBox.setText(self.config["last_path"])
            self.refresh()

    # ================================
    # PATH
    # ================================
    def browse(self):
        p = QFileDialog.getExistingDirectory(self)
        if p:
            self.pathBox.setText(p)
            self.config["last_path"] = p
            save_json(CONFIG_FILE, self.config)
            self.refresh()

    def auto_detect(self):
        libs = get_steam_libraries()

        if not libs:
            self.status.setText("No Steam libraries found on any drive")
            return

        # Remove duplicates just in case
        libs = list(set(libs))

        # If only one, auto-select
        if len(libs) == 1:
            self.pathBox.setText(libs[0])
            self.config["last_path"] = libs[0]
            save_json(CONFIG_FILE, self.config)
            self.refresh()
            return

        # Multiple found → let user choose
        choice, ok = QInputDialog.getItem(
            self,
            "Select Steam Library",
            "Choose a Steam library:",
            libs,
            0,
            False
        )

        if ok and choice:
            self.pathBox.setText(choice)
            self.config["last_path"] = choice
            save_json(CONFIG_FILE, self.config)
            self.refresh()

    # ================================
    # HASH
    # ================================
    def check_hash(self, file, expected):
        if file in self.cache and self.cache[file] == expected:
            return True

        if not os.path.isfile(file):
            return False

        h = md5(open(file, "rb").read()).hexdigest().upper()
        self.cache[file] = h
        return h == expected

    # ================================
    # LIST
    # ================================
    def refresh(self):
        self.listWidget.clear()

        base = self.pathBox.text()
        if not os.path.isdir(base):
            return

        games = [g for g in os.listdir(base) if os.path.isdir(os.path.join(base, g))]
        game_map = build_map(games)

        for patch in ALL_PATCHES:
            match = find_match(patch["game"], game_map)

            status = "Not Installed"
            if match:
                status = "Patched"

                for f, h in patch["hashes"].items():
                    if not self.check_hash(os.path.join(base, match, "game", f), h):
                        status = "Unpatched"
                        break

            item = QListWidgetItem()
            item.setData(Qt.UserRole, {
                "patch": patch,
                "name": patch["game"],
                "status": status,
                "selected": status == "Unpatched"
            })

            self.update_item(item)
            self.listWidget.addItem(item)

        save_json(CACHE_FILE, self.cache)

    def update_item(self, item):
        d = item.data(Qt.UserRole)
        icon = "✔" if d["selected"] else "✖"
        item.setText(f"{icon} {d['name']} [{d['status']}]")

        colors = {
            "Patched": "#57F287",
            "Unpatched": "#FEE75C",
            "Not Installed": "#ED4245"
        }
        item.setForeground(QColor(colors[d["status"]]))

    def toggle(self, item):
        d = item.data(Qt.UserRole)
        d["selected"] = not d["selected"]
        item.setData(Qt.UserRole, d)
        self.update_item(item)

    def filter(self):
        q = self.search.text().lower()
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            item.setHidden(q not in item.text().lower())

    # ================================
    # PATCHING
    # ================================
    def start_worker(self, data):
        base = self.pathBox.text()
        games = os.listdir(base)
        game_map = build_map(games)

        match = find_match(data["name"], game_map)
        if not match:
            return

        worker = PatchWorker(data["patch"], os.path.join(base, match))

        worker.signals.progress.connect(self.update_progress)
        worker.signals.done.connect(self.done)
        worker.signals.error.connect(self.error)

        self.pool.start(worker)

    def patch_selected(self):
        for i in range(self.listWidget.count()):
            d = self.listWidget.item(i).data(Qt.UserRole)
            if d["selected"]:
                self.start_worker(d)

    def patch_all(self):
        for i in range(self.listWidget.count()):
            d = self.listWidget.item(i).data(Qt.UserRole)
            if d["status"] == "Unpatched":
                self.start_worker(d)

    def update_progress(self, name, value):
        self.status.setText(f"{name} {value}%")
        self.progress.setValue(value)

    def done(self, name):
        self.status.setText(f"{name} done")
        self.refresh()

    def error(self, msg):
        self.status.setText(msg)

# ================================
# THEME
# ================================
def theme(app):
    app.setStyle("Fusion")
    app.setStyleSheet("""
    QWidget { background:#2f3136; color:#dcddde; }
    QPushButton { background:#5865F2; color:white; padding:6px; }
    QLineEdit { background:#202225; padding:5px; }
    """)

# ================================
# ENTRY
# ================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    theme(app)

    win = SakuraPatcher()
    win.show()

    sys.exit(app.exec_())