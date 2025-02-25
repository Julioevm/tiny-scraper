from pathlib import Path
from typing import List, Optional
from main import hw_info, system_lang
from graphic import screen_resolutions
from language import Translator
import graphic as gr
import input
import sys
import time
import socket
from anbernic import Anbernic
from scraper import Scraper
from systems import get_system_id

translator = Translator(system_lang)
selected_position = 0
roms_selected_position = 0
selected_system = ""
current_window = "console"
an = Anbernic()
scraper = Scraper()
skip_input_check = False

x_size, y_size ,max_elem = screen_resolutions.get(hw_info, (640, 480, 11))

button_x = x_size - 110
button_y = y_size - 30
ratio = y_size / x_size


def is_connected():
    try:
        sock = socket.create_connection(("1.1.1.1", 53), timeout=3)
        sock.close()
        return True
    except (socket.timeout, socket.error):
        return False


def start(config_path: str) -> None:
    print("Starting Tiny Scraper...")
    if not is_connected():
        gr.draw_log(
            f"{translator.translate('No internet connection')}", fill=gr.colorBlue, outline=gr.colorBlueD1
        )
        gr.draw_paint()
        time.sleep(3)
        sys.exit(1)
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
            selected_position += input.value
            if selected_position < 0:
                selected_position = len(available_systems) - 1
            elif selected_position >= len(available_systems):
                selected_position = 0
        elif input.key("A"):
            selected_system = available_systems[selected_position]
            current_window = "roms"
            gr.draw_log(
                f"{translator.translate('Checking existing media...')}", fill=gr.colorBlue, outline=gr.colorBlueD1
            )
            gr.draw_paint()
            skip_input_check = True
            return

    if input.key("Y"):
        an.switch_sd_storage()
        selected_position = 0
        available_systems = scraper.get_available_systems(an.get_sd_storage_path())

    gr.draw_clear()

    gr.draw_rectangle_r([10, 40, x_size - 10, y_size - 40], 15, fill=gr.colorGrayD2, outline=None)
    gr.draw_text((x_size / 2, 20), f"{translator.translate('Tiny Scraper')}", font=17, anchor="mm")

    if len(available_systems) > 1:
        start_idx = int(selected_position / max_elem) * max_elem
        end_idx = start_idx + max_elem
        for i, system in enumerate(available_systems[start_idx:end_idx]):
            row_list(
                system, (20, 50 + (i * 35)), x_size - 40, i == (selected_position % max_elem)
            )
        button_circle((30, button_y), "A", f"{translator.translate('Select')}")
    else:
        gr.draw_text(
            (x_size / 2, y_size / 2), f"{translator.translate('No roms found in TF')} {an.get_sd_storage()}", anchor="mm"
        )

    button_circle((button_x-110, button_y), "Y", f"TF: {an.get_sd_storage()}")
    button_circle((button_x, button_y), "M", f"{translator.translate('Exit')}")

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
    roms_without_image.sort(key=lambda x: x.name)
    system_id = get_system_id(selected_system)

    if len(roms_without_image) < 1:
        current_window = "console"
        selected_system = ""
        gr.draw_log(
            f"{translator.translate('No roms missing media found...')}", fill=gr.colorBlue, outline=gr.colorBlueD1
        )
        gr.draw_paint()
        time.sleep(2)
        gr.draw_clear()
        exit_menu = True

    if input.key("B"):
        exit_menu = True
    elif input.key("A"):
        gr.draw_log(f"{translator.translate('Scraping...')}", fill=gr.colorBlue, outline=gr.colorBlueD1)
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
                f"{translator.translate('Scraping completed')}", fill=gr.colorBlue, outline=gr.colorBlueD1
            )
            print(f"Done scraping {rom.name}. Saved file to {img_path}")
        else:
            gr.draw_log(f"{translator.translate('Scraping failed!')}", fill=gr.colorBlue, outline=gr.colorBlueD1)
            print(f"Failed to get screenshot for {rom.name}")
        gr.draw_paint()
        time.sleep(3)
        exit_menu = True
    elif input.key("START"):
        progress: int = 1
        success: int = 0
        failure: int = 0
        gr.draw_log(
            f"{translator.translate('Scraping')} {progress} {translator.translate('of')} {len(roms_without_image)}",
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
                    f"{translator.translate('Scraping')} {progress} {translator.translate('of')} {len(roms_without_image)}",
                    fill=gr.colorBlue,
                    outline=gr.colorBlueD1,
                )
                gr.draw_paint()
        gr.draw_log(
            f"{translator.translate('Scraping completed! Success:')} {success} {translator.translate('Errors:')} {failure}",
            fill=gr.colorBlue,
            outline=gr.colorBlueD1,
            width=800,
        )
        gr.draw_paint()
        time.sleep(4)
        exit_menu = True
    elif input.key("DY"):
        roms_selected_position += input.value
        if roms_selected_position < 0:
            roms_selected_position = len(roms_without_image) - 1
        elif roms_selected_position >= len(roms_without_image):
            roms_selected_position = 0
    elif input.key("L1"):
        if roms_selected_position > 0:
            roms_selected_position = max(0, roms_selected_position - max_elem)
    elif input.key("R1"):
        if roms_selected_position < len(roms_without_image) - 1:
            roms_selected_position = min(
                len(roms_without_image) - 1, roms_selected_position + max_elem
            )
    elif input.key("L2"):
        if roms_selected_position > 0:
            roms_selected_position = max(0, roms_selected_position - 100)
    elif input.key("R2"):
        if roms_selected_position < len(roms_without_image) - 1:
            roms_selected_position = min(
                len(roms_without_image) - 1, roms_selected_position + 100
            )

    if exit_menu:
        current_window = "console"
        selected_system = ""
        gr.draw_clear()
        roms_selected_position = 0
        skip_input_check = True
        return

    gr.draw_clear()

    gr.draw_rectangle_r([10, 40, x_size - 10, y_size - 40], 15, fill=gr.colorGrayD2, outline=None)
    gr.draw_text(
        (x_size / 2, 20),
        f"{selected_system} - {translator.translate('Roms:')} {len(roms_list)} {translator.translate('Missing media:')} {len(roms_without_image)}",
        anchor="mm",
    )

    start_idx = int(roms_selected_position / max_elem) * max_elem
    end_idx = start_idx + max_elem
    for i, rom in enumerate(roms_without_image[start_idx:end_idx]):
        row_list(
            rom.name[:48] + "..." if len(rom.name) > 50 else rom.name,
            (20, 50 + (i * 35)),
            x_size -40,
            i == (roms_selected_position % max_elem),
        )

    button_rectangle((20, button_y), "Start", f"{translator.translate('D. All')}")
    button_circle((190, button_y), "A", f"{translator.translate('Download')}")
    button_circle((320, button_y), "B", f"{translator.translate('Back')}")
    button_circle((button_x, button_y), "M", f"{translator.translate('Exit')}")

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
