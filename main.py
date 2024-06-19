import os
import requests
import binascii
import json
from pathlib import Path

from rom import Rom

CONFIG_PATH = "config.json"
USER = ""
PASSWORD = ""

# List of systems
systems = ["PSX", "GB", "GBC", "FC", "SFC", "MD"]

def load_config_from_json(filepath) -> bool:
    global USER, PASSWORD
    if not os.path.exists(filepath):
        print(f"Config file {filepath} not found.")
        return False
    
    with open(filepath, 'r') as file:
        config = json.load(file)
        USER = config.get("user")
        PASSWORD = config.get("password")
        
    return True

def crc32_from_file(rom: str):
    buf = rom.open(mode='rb').read()
    buf = (binascii.crc32(buf) & 0xFFFFFFFF)
    return "%08X" % buf

def get_roms(path: str) -> list[Rom]:
    roms = []
    for file in os.listdir(path):
        if file.endswith(".sfc"):
            name = file[:-4]
            rom = Rom(filename=file, name=name, crc=crc32_from_file(Path(path) / file))
            roms.append(rom)
            print(f"Added {rom.name} to list.")
    return roms

def prompt_user_for_systems(systems):
    # Temporal solution for testing
    selected_systems = []
    print("Select systems to use (type the number and press Enter, leave empty when finished):")
    for i, system in enumerate(systems, 1):
        print(f"{i}. {system}")

    while True:
        choice = input("Enter choice: ")
        if choice.lower() == '':
            break
        try:
            index = int(choice) - 1
            if 0 <= index < len(systems):
                if systems[index] not in selected_systems:
                    selected_systems.append(systems[index])
                    print(f"{systems[index]} added to selection.")
                else:
                    print(f"{systems[index]} is already selected.")
            else:
                print("Invalid choice, try again.")
        except ValueError:
            print("Invalid input, try again.")

    return selected_systems

def get_files_without_extension(folder):
    return [f.stem for f in Path(folder).glob('*') if f.is_file()]

def scrape_screenshot(game_name: str, crc: str = None, system_id: int = 1):
    url = f"https://api.screenscraper.fr/api2/jeuInfos.php?devid=xxx&devpassword=yyy&softname=tiny-scraper&output=json&ssid={USER}&sspassword={PASSWORD}&crc=50ABC90A&systemeid={system_id}&romtype=rom&romnom={game_name}"

    response = requests.get(url)
    if response.status_code == 200:
        try:
            screenshot_url = ""
            data = response.json()
            game_data = data.get("response").get("jeu")


            screenshot_url = ""
            for media in game_data.get('medias'):
                if media["type"] == "ss":
                    screenshot_url = media["url"]
                    break

            if screenshot_url:
                img_response = requests.get(screenshot_url)

                if img_response.headers.get('content-type') == 'image/png':
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

    for system in selected_systems:
        system_path = Path('Roms/' + system)
        if not system_path.exists():
            print(f"Folder for {system} does not exist. Skipping...")
            continue
        
        # List files in the system folder
        system_files = get_files_without_extension(system_path)

        # Check for Imgs folder
        imgs_folder = system_path / "Imgs"
        if not imgs_folder.exists():
            imgs_folder.mkdir()
            imgs_files = []
        else:
            imgs_files = get_files_without_extension(imgs_folder)

        # Compare lists
        missing_files = [f for f in system_files if f not in imgs_files]
        print(f"{len(missing_files)} files are missing in {imgs_folder} for {system}.")

        # Scrape screenshots for missing files
        for game_name in missing_files:
            screenshot = scrape_screenshot(game_name)
            if screenshot:
                img_path = imgs_folder / f"{game_name}.png"
                with open(img_path, 'wb') as img_file:
                    img_file.write(screenshot)
                print(f"Saved screenshot for {game_name} in {imgs_folder}")

if __name__ == "__main__":
    main()
