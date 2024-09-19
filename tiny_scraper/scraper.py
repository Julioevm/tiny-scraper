import os
import binascii
import json
import base64
from pathlib import Path
from urllib.request import urlopen, Request
from systems import get_system_extension, systems
from rom import Rom

USER = ""
PASSWORD = ""
DEVID = ""
DEVPASSWORD = ""
MEDIA_TYPE = "ss"


def load_config_from_json(filepath) -> bool:
    global USER, PASSWORD, DEVID, DEVPASSWORD, MEDIA_TYPE
    if not os.path.exists(filepath):
        return False

    with open(filepath, "r") as file:
        config = json.load(file)
        USER = config.get("user")
        PASSWORD = config.get("password")
        DEVID = config.get("devid")
        DEVPASSWORD = config.get("devpassword")
        MEDIA_TYPE = config.get("media_type") or "ss"

    return True


def crc32_from_file(rom):
    buf = rom.open(mode="rb").read()
    buf = binascii.crc32(buf) & 0xFFFFFFFF
    return "%08X" % buf


def get_roms(path, system: str) -> list[Rom]:
    roms = []
    system_extensions = get_system_extension(system)
    for file in os.listdir(path):
        if file.endswith(tuple(system_extensions)):
            name = file[:-4]
            rom = Rom(filename=file, name=name, crc=crc32_from_file(Path(path) / file))
            roms.append(rom)
            
    return roms

def available_systems(rom_path: str) -> list[str] | None:
    all_systems = [system["name"] for system in systems]
    # Check that the system folders exist and have roms
    available_systems = []
    for system in all_systems:
        system_path = Path(rom_path) / system
        if system_path.exists() and any(system_path.iterdir()):
            available_systems.append(system)


def get_files_without_extension(folder):
    return [f.stem for f in Path(folder).glob("*") if f.is_file()]

def get_image_files_without_extension(folder):
    image_extensions = (".jpg", ".jpeg", ".png")
    return [f.stem for f in folder.glob("*") if f.suffix.lower() in image_extensions]

def scrape_screenshot(crc: str, game_name: str, system_id: int) -> bytes | None:
    decoded_devid = base64.b64decode(DEVID).decode()
    decoded_devpassword = base64.b64decode(DEVPASSWORD).decode()
    url = f"https://api.screenscraper.fr/api2/jeuInfos.php?devid={decoded_devid}&devpassword={decoded_devpassword}&softname=tiny-scraper&output=json&ssid={USER}&sspassword={PASSWORD}&crc={crc}&systemeid={system_id}&romtype=rom&romnom={game_name}"

    print(f"Scraping screenshot for {game_name}...")
    request = Request(url)
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


