from pathlib import Path
from typing import List, Optional
import graphic as gr
import input
import sys
import time
from anbernic import Anbernic

from scraper import Scraper
from systems import get_system_id

selected_position = 0
roms_selected_position = 0
selected_system = ""
current_window = "console"
max_elem = 11
an = Anbernic()
scraper = Scraper()
skip_input_check = False


def start(config_path: str) -> None:
    print("Starting Tiny Scraper...")
    scraper.load_config_from_json(config_path)
    load_console_menu()


def update() -> None:
    global current_window, selected_position, skip_input_check

    if skip_input_check:
        input.reset_input()
        skip_input_check = False
    else:
        input.check()

    if input.key("MENUF"):
        gr.draw_end()
        print("Exiting Tiny Scraper...")
        sys.exit()

    if current_window == "console":
        load_console_menu()
    elif current_window == "roms":
        load_roms_menu()
    else:
        load_console_menu()


def load_console_menu() -> None:
    global selected_position, selected_system, current_window, skip_input_check

    available_systems = scraper.get_available_systems(an.get_sd_storage_path())

    if available_systems:
        if input.key("DY"):
            if input.value == 1:
                if selected_position < len(available_systems) - 1:
                    selected_position += 1
            elif input.value == -1:
                if selected_position > 0:
                    selected_position -= 1
        elif input.key("A"):
            selected_system = available_systems[selected_position]
            current_window = "roms"
            gr.draw_log(
                "Checking existing media...", fill=gr.colorBlue, outline=gr.colorBlueD1
            )
            gr.draw_paint()
            skip_input_check = True
            return

    if input.key("Y"):
        an.switch_sd_storage()

    gr.draw_clear()

    gr.draw_rectangle_r([10, 40, 630, 440], 15, fill=gr.colorGrayD2, outline=None)
    gr.draw_text((320, 20), "Tiny Scraper", anchor="mm")

    if len(available_systems) > 1:
        start_idx = int(selected_position / max_elem) * max_elem
        end_idx = start_idx + max_elem
        for i, system in enumerate(available_systems[start_idx:end_idx]):
            row_list(
                system, (20, 50 + (i * 35)), 600, i == (selected_position % max_elem)
            )
        button_circle((30, 450), "A", "Select")
    else:
        gr.draw_text(
            (320, 240), f"No roms found in SD {an.get_sd_storage()}", anchor="mm"
        )

    button_circle((133, 450), "M", "Exit")
    button_circle((355, 450), "Y", f"SD: {an.get_sd_storage()}")

    gr.draw_paint()


def load_roms_menu() -> None:
    global \
        selected_position, \
        current_window, \
        roms_selected_position, \
        skip_input_check, \
        selected_system

    exit_menu = False
    roms_list = scraper.get_roms(an.get_sd_storage_path(), selected_system)
    system_path = Path(an.get_sd_storage_path()) / selected_system
    imgs_folder = Path(f"{an.get_sd_storage_path()}/{selected_system}/Imgs")

    if not imgs_folder.exists():
        imgs_folder.mkdir()
        imgs_files: List[str] = []
    else:
        imgs_files = scraper.get_image_files_without_extension(imgs_folder)

    roms_without_image = list(set([rom for rom in roms_list if rom.name not in imgs_files]))
    system_id = get_system_id(selected_system)

    if len(roms_without_image) < 1:
        current_window = "console"
        selected_system = ""
        gr.draw_log(
            "No roms missing media found...", fill=gr.colorBlue, outline=gr.colorBlueD1
        )
        gr.draw_paint()
        time.sleep(2)
        gr.draw_clear()
        exit_menu = True

    if input.key("B"):
        exit_menu = True
    elif input.key("A"):
        gr.draw_log("Scraping...", fill=gr.colorBlue, outline=gr.colorBlueD1)
        gr.draw_paint()
        rom = roms_without_image[roms_selected_position]
        rom.set_crc(scraper.get_crc32_from_file(system_path / rom.filename))
        screenshot = scraper.scrape_screenshot(
            game_name=rom.name, crc=rom.crc, system_id=system_id
        )
        if screenshot:
            img_path: Path = imgs_folder / f"{rom.name}.png"
            img_path.write_bytes(screenshot)
            gr.draw_log(
                "Scraping completed!", fill=gr.colorBlue, outline=gr.colorBlueD1
            )
            print(f"Done scraping {rom.name}. Saved file to {img_path}")
        else:
            gr.draw_log("Scraping failed!", fill=gr.colorBlue, outline=gr.colorBlueD1)
            print(f"Failed to get screenshot for {rom.name}")
        gr.draw_paint()
        time.sleep(3)
        exit_menu = True
    elif input.key("START"):
        progress: int = 0
        success: int = 0
        failure: int = 0
        gr.draw_log(
            f"Scraping {progress} of {len(roms_without_image)}",
            fill=gr.colorBlue,
            outline=gr.colorBlueD1,
        )
        gr.draw_paint()
        for rom in roms_without_image:
            if rom.name not in imgs_files:
                rom.set_crc(scraper.get_crc32_from_file(system_path / rom.filename))
                screenshot: Optional[bytes] = scraper.scrape_screenshot(
                    game_name=rom.name, crc=rom.crc, system_id=system_id
                )
                if screenshot:
                    img_path: Path = imgs_folder / f"{rom.name}.png"
                    img_path.write_bytes(screenshot)
                    print(f"Done scraping {rom.name}. Saved file to {img_path}")
                    success += 1
                else:
                    print(f"Failed to get screenshot for {rom.name}")
                    failure += 1
                progress += 1
                gr.draw_log(
                    f"Scraping {progress} of {len(roms_without_image)}",
                    fill=gr.colorBlue,
                    outline=gr.colorBlueD1,
                )
                gr.draw_paint()
        gr.draw_log(
            f"Scraping completed! Success: {success} Errors: {failure}",
            fill=gr.colorBlue,
            outline=gr.colorBlueD1,
            width=800,
        )
        gr.draw_paint()
        time.sleep(4)
        exit_menu = True
    elif input.key("Y"):
        an.switch_sd_storage()
    elif input.key("DY"):
        if input.value == 1:
            if roms_selected_position < len(roms_list) - 1:
                roms_selected_position += 1
        elif input.value == -1:
            if roms_selected_position > 0:
                roms_selected_position -= 1
    elif input.key("L1"):
        if roms_selected_position > 0:
            roms_selected_position = max(0, roms_selected_position - max_elem)
    elif input.key("R1"):
        if roms_selected_position < len(roms_list) - 1:
            roms_selected_position = min(
                len(roms_list) - 1, roms_selected_position + max_elem
            )
    elif input.key("L2"):
        if roms_selected_position > 0:
            roms_selected_position = max(0, roms_selected_position - 100)
    elif input.key("R2"):
        if roms_selected_position < len(roms_list) - 1:
            roms_selected_position = min(
                len(roms_list) - 1, roms_selected_position + 100
            )

    if exit_menu:
        current_window = "console"
        selected_system = ""
        gr.draw_clear()
        roms_selected_position = 0
        skip_input_check = True
        return

    gr.draw_clear()

    gr.draw_rectangle_r([10, 40, 630, 440], 15, fill=gr.colorGrayD2, outline=None)
    gr.draw_text(
        (320, 10),
        f"{selected_system} - Roms: {len(roms_list)} Missing media: {len(roms_without_image)}",
        anchor="mm",
    )

    start_idx = int(roms_selected_position / max_elem) * max_elem
    end_idx = start_idx + max_elem
    for i, rom in enumerate(roms_without_image[start_idx:end_idx]):
        row_list(
            rom.name[:48] + "..." if len(rom.name) > 50 else rom.name,
            (20, 50 + (i * 35)),
            600,
            i == (roms_selected_position % max_elem),
        )

    button_rectangle((30, 450), "Start", "D. All")
    button_circle((170, 450), "A", "Download")
    button_circle((300, 450), "B", "Back")
    button_circle((390, 450), "Y", f"SD: {an.get_sd_storage()}")
    button_circle((480, 450), "M", "Exit")

    gr.draw_paint()


def row_list(text: str, pos: tuple[int, int], width: int, selected: bool) -> None:
    gr.draw_rectangle_r(
        [pos[0], pos[1], pos[0] + width, pos[1] + 32],
        5,
        fill=(gr.colorBlue if selected else gr.colorGrayL1),
    )
    gr.draw_text((pos[0] + 5, pos[1] + 5), text)


def button_circle(pos: tuple[int, int], button: str, text: str) -> None:
    gr.draw_circle(pos, 25, fill=gr.colorBlueD1)
    gr.draw_text((pos[0] + 12, pos[1] + 12), button, anchor="mm")
    gr.draw_text((pos[0] + 30, pos[1] + 12), text, font=13, anchor="lm")


def button_rectangle(pos: tuple[int, int], button: str, text: str) -> None:
    gr.draw_rectangle_r(
        (pos[0], pos[1], pos[0] + 60, pos[1] + 25), 5, fill=gr.colorGrayL1
    )
    gr.draw_text((pos[0] + 30, pos[1] + 12), button, anchor="mm")
    gr.draw_text((pos[0] + 65, pos[1] + 12), text, font=13, anchor="lm")
