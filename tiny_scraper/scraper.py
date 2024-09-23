import os
import binascii
import json
import base64
from pathlib import Path
from urllib.request import urlopen, Request
import urllib.parse
from systems import get_system_extension, systems

USER = ""
PASSWORD = ""
DEVID = "cmVhdmVu"
DEVPASSWORD = "MDZXZUY5bTBldWs="
MEDIA_TYPE = "ss"


class Rom:
    def __init__(self, name, filename, crc=""):
        self.name = name
        self.filename = filename
        self.crc = crc

    def set_crc(self, crc):
        self.crc = crc


def load_config_from_json(filepath) -> bool:
    global USER, PASSWORD, MEDIA_TYPE
    if not os.path.exists(filepath):
        print(f"Config file {filepath} not found")
        return False

    with open(filepath, "r") as file:
        config = json.load(file)
        USER = config.get("user")
        PASSWORD = config.get("password")
        MEDIA_TYPE = config.get("media_type") or "ss"

    return True


def get_crc32_from_file(rom):
    buf = rom.open(mode="rb").read()
    buf = binascii.crc32(buf) & 0xFFFFFFFF
    return "%08X" % buf


def get_roms(path, system: str) -> list[Rom]:
    roms = []
    system_path = Path(path) / system
    system_extensions = get_system_extension(system)
    if not system_extensions:
        print(f"No extensions found for system: {system}")
        return roms

    for file in os.listdir(system_path):
        file_path = Path(system_path) / file
        if file.startswith("."):
            continue
        if file_path.is_file():
            file_extension = file_path.suffix.lower().lstrip(".")
            if file_extension in system_extensions:
                name = file_path.stem
                rom = Rom(filename=file, name=name)
                roms.append(rom)

    return roms


# Check that the system folders exist and have roms
def get_available_systems(roms_path: str) -> list[str]:
    all_systems = [system["name"] for system in systems]
    available_systems = []
    for system in all_systems:
        system_path = Path(roms_path) / system
        if system_path.exists() and any(system_path.iterdir()):
            available_systems.append(system)

    return available_systems


def get_files_without_extension(folder):
    return [f.stem for f in Path(folder).glob("*") if f.is_file()]


def get_image_files_without_extension(folder):
    image_extensions = (".jpg", ".jpeg", ".png")
    return [f.stem for f in folder.glob("*") if f.suffix.lower() in image_extensions]


def scrape_screenshot(crc: str, game_name: str, system_id: int) -> bytes | None:
    decoded_devid = base64.b64decode(DEVID).decode()
    decoded_devpassword = base64.b64decode(DEVPASSWORD).decode()
    # URL-encode the game_name parameter
    encoded_game_name = urllib.parse.quote(game_name)
    url = f"https://api.screenscraper.fr/api2/jeuInfos.php?devid={decoded_devid}&devpassword={decoded_devpassword}&softname=tiny-scraper&output=json&ssid={USER}&sspassword={PASSWORD}&crc={crc}&systemeid={system_id}&romtype=rom&romnom={encoded_game_name}"

    print(f"Scraping screenshot for {game_name}...")
    request = Request(url)
    try:
        with urlopen(request) as response:
            if response.status == 200:
                try:
                    data = json.loads(response.read())
                    game_data = data.get("response").get("jeu")

                    screenshot_url = ""
                    for media in game_data.get("medias"):
                        if media["type"] == MEDIA_TYPE:
                            screenshot_url = media["url"]
                            break

                    if screenshot_url:
                        img_request = Request(screenshot_url)
                        with urlopen(img_request) as img_response:
                            if img_response.headers.get("Content-Type") == "image/png":
                                return img_response.read()
                            else:
                                print(f"Invalid image format for {game_name}")
                    else:
                        print(f"No screenshot URL found for {game_name}")
                except ValueError:
                    print(f"Invalid JSON response for {game_name}")
            else:
                print(f"Failed to get screenshot for {game_name}")
        return None
    # Any other exception return the error and log the url used
    except Exception as e:
        print(f"Error scraping screenshot for {game_name}: {e}")
        print(f"URL used: {url}")
        return None
