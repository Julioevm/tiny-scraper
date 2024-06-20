import os
import requests
import binascii
import json
import base64
from pathlib import Path
from simple_term_menu import TerminalMenu
from systems import get_system_extension, get_system_id, systems
from rom import Rom

CONFIG_PATH = "config.json"
USER = ""
PASSWORD = ""
DEVID = ""
DEVPASSWORD = ""
MEDIA_TYPE = "ss"

# List of systems
systems = ["PSX", "GB", "GBC", "FC", "SFC", "MD"]


def load_config_from_json(filepath) -> bool:
    global USER, PASSWORD, DEVID, DEVPASSWORD, MEDIA_TYPE
    if not os.path.exists(filepath):
        print(f"Config file {filepath} not found.")
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
            
    print(f"Found {len(roms)} roms for {system}.")
    return roms


def prompt_user_for_systems(systems):
    terminal_menu = TerminalMenu(
        systems,
        multi_select=True,
        show_multi_select_hint=True,
        title="Select systems to find media:",
    )
    terminal_menu.show()

    return terminal_menu.chosen_menu_entries


def get_files_without_extension(folder):
    return [f.stem for f in Path(folder).glob("*") if f.is_file()]

def get_image_files_without_extension(folder):
    image_extensions = (".jpg", ".jpeg", ".png")
    return [f.stem for f in folder.glob("*") if f.suffix.lower() in image_extensions]

def scrape_screenshot(game_name: str, crc: str, system_id: int):
    decoded_devid = base64.b64decode(DEVID).decode()
    decoded_devpassword = base64.b64decode(DEVPASSWORD).decode()
    url = f"https://api.screenscraper.fr/api2/jeuInfos.php?devid={decoded_devid}&devpassword={decoded_devpassword}&softname=tiny-scraper&output=json&ssid={USER}&sspassword={PASSWORD}&crc=50ABC90A&systemeid={system_id}&romtype=rom&romnom={game_name}"

    print(f"Scraping screenshot for {game_name}...")
    response = requests.get(url)
    if response.status_code == 200:
        try:
            screenshot_url = ""
            data = response.json()
            game_data = data.get("response").get("jeu")

            screenshot_url = ""
            for media in game_data.get("medias"):
                if media["type"] == MEDIA_TYPE:
                    screenshot_url = media["url"]
                    break

            if screenshot_url:
                img_response = requests.get(screenshot_url)

                if img_response.headers.get("content-type") == "image/png":
                    return img_response.content
                else:
                    print(f"Invalid image format for {game_name}")
            else:
                print(f"No screenshot URL found for {game_name}")
        except ValueError:
            print(f"Invalid JSON response for {game_name}")
    else:
        print(f"Failed to get screenshot for {game_name}")
    return None


def main():
    if not load_config_from_json(CONFIG_PATH):
        return

    selected_systems = prompt_user_for_systems(systems)

    if not selected_systems:
        print("No systems selected. Exiting...")
        return

    for system in selected_systems:
        system_path = Path("Roms/" + system)
        if not system_path.exists():
            print(f"Folder for {system} does not exist. Skipping...")
            continue

        roms = get_roms(system_path, system)

        imgs_folder = system_path / "Imgs"
        if not imgs_folder.exists():
            imgs_folder.mkdir()
            imgs_files = []
        else:
            imgs_files = get_image_files_without_extension(imgs_folder)

        missing_files = [rom.name for rom in roms if rom.name not in imgs_files]
        
        if len(missing_files) == 0:
            print(f"All files are already present for {system} have images.")
            continue
            
        print(f"{len(missing_files)} files are missing in {imgs_folder} for {system}.")

        system_id = get_system_id(system)
        
        # TODO: only scrape missing files
        for rom in roms:
            screenshot = scrape_screenshot(
                game_name=rom.name, crc=rom.crc, system_id=system_id
            )
            if screenshot:
                img_path = imgs_folder / f"{rom.name}.png"
                with open(img_path, "wb") as img_file:
                    img_file.write(screenshot)
                print(f"Done scraping {rom.name}.")


if __name__ == "__main__":
    main()
