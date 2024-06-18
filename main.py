import os
import requests
from pathlib import Path

# Hardcoded user and password for screenscraper.fr API
USER = 'your_username'
PASSWORD = 'your_password'

# List of systems
systems = ["PSX", "GB", "GBC", "FC", "SFC"]

def prompt_user_for_systems(systems):
    selected_systems = []
    print("Select systems to use (type the number and press Enter, type 'done' when finished):")
    for i, system in enumerate(systems, 1):
        print(f"{i}. {system}")
    
    while True:
        choice = input("Enter choice: ")
        if choice.lower() == 'done':
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

def scrape_screenshot(game_name):
    url = f"https://www.screenscraper.fr/api2/media.php?devid=YOUR_DEV_ID&devpassword=YOUR_DEV_PASSWORD&softname=YOUR_SOFT_NAME&output=json&ssid={USER}&sspassword={PASSWORD}&media=ss&game={game_name}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            screenshot_url = data.get('url')
            if screenshot_url:
                img_response = requests.get(screenshot_url)
                if img_response.status_code == 200:
                    return img_response.content
                else:
                    print(f"Failed to download image for {game_name}")
            else:
                print(f"No screenshot URL found for {game_name}")
        except ValueError:
            print(f"Invalid JSON response for {game_name}")
    else:
        print(f"Failed to get screenshot for {game_name}")
    return None

def main():
    selected_systems = prompt_user_for_systems(systems)
    
    for system in selected_systems:
        system_path = Path(system)
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