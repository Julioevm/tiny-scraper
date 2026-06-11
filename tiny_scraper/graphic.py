import ctypes
import os
from main import hw_info, hdmi_info
from typing import Optional

import sdl2
from PIL import Image, ImageDraw, ImageFont

script_dir = os.path.dirname(os.path.abspath(__file__))
local_font_list = os.path.join(script_dir, "font/font.ttf")
sys_font_file = os.path.join("/mnt/vendor/bin/default.ttf")
fallback_font = "/usr/share/fonts/TTF/DejaVuSansMono.ttf"
font_file = local_font_list if os.path.exists(local_font_list) else (
    sys_font_file if os.path.exists(sys_font_file) else fallback_font
)

screen_resolutions = {
    1: (720, 720, 18),
    2: (720, 480, 11),
}


class UserInterface:
    _instance: Optional["UserInterface"] = None
    _initialized: bool = False

    screen_width, screen_height, max_elem = screen_resolutions.get(hw_info, (640, 480, 11))
    colorBlue = "#bb7200"
    colorBlueD1 = "#7f4f00"
    colorGray = "#292929"
    colorGrayL1 = "#383838"
    colorGrayD2 = "#141414"

    active_image: Image.Image
    active_draw: ImageDraw.ImageDraw

    def __init__(self):
        if self._initialized:
            return
        self.window = self._create_window()
        self.renderer = self._create_renderer()
        self.draw_start()
        self._initialized = True

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(UserInterface, cls).__new__(cls)
        return cls._instance

    ###
    # WINDOW MANAGEMENT
    ###

    def create_image(self):
        return Image.new("RGBA", (self.screen_width, self.screen_height), color="black")

    def draw_start(self):
        sdl2.SDL_SetRenderDrawColor(self.renderer, 0, 0, 0, 255)
        sdl2.SDL_RenderClear(self.renderer)
        self.active_image = self.create_image()
        self.active_draw = ImageDraw.Draw(self.active_image)

    def _create_window(self):
        window = sdl2.SDL_CreateWindow(
            "Tiny Scraper".encode("utf-8"),
            sdl2.SDL_WINDOWPOS_UNDEFINED,
            sdl2.SDL_WINDOWPOS_UNDEFINED,
            0,
            0,
            sdl2.SDL_WINDOW_FULLSCREEN_DESKTOP | sdl2.SDL_WINDOW_SHOWN,
        )
        if not window:
            print(f"Failed to create window: {sdl2.SDL_GetError()}")
            raise RuntimeError("Failed to create window")
        return window

    def _create_renderer(self):
        renderer = sdl2.SDL_CreateRenderer(
            self.window, -1, sdl2.SDL_RENDERER_ACCELERATED
        )
        if not renderer:
            renderer = sdl2.SDL_CreateRenderer(
                self.window, -1, sdl2.SDL_RENDERER_SOFTWARE
            )
            if not renderer:
                print(f"Failed to create renderer: {sdl2.SDL_GetError()}")
                raise RuntimeError("Failed to create renderer")
        sdl2.SDL_SetHint(sdl2.SDL_HINT_RENDER_SCALE_QUALITY, b"0")
        return renderer

    def draw_paint(self):
        if hw_info == 3 and hdmi_info != "HDMI=1":
            rotated_image = self.active_image.rotate(90, expand=True)
            rgba_data = rotated_image.tobytes()
            temp_width, temp_height = rotated_image.size
        else:
            rgba_data = self.active_image.tobytes()
            temp_width, temp_height = self.screen_width, self.screen_height

        surface = sdl2.SDL_CreateRGBSurfaceWithFormatFrom(
            rgba_data,
            temp_width,
            temp_height,
            32,
            temp_width * 4,
            sdl2.SDL_PIXELFORMAT_RGBA32,
        )
        texture = sdl2.SDL_CreateTextureFromSurface(self.renderer, surface)
        sdl2.SDL_FreeSurface(surface)

        window_width = ctypes.c_int()
        window_height = ctypes.c_int()
        sdl2.SDL_GetWindowSize(
            self.window, ctypes.byref(window_width), ctypes.byref(window_height)
        )
        window_width, window_height = window_width.value, window_height.value

        dst_rect = sdl2.SDL_Rect(0, 0, window_width, window_height)
        sdl2.SDL_RenderCopy(self.renderer, texture, None, dst_rect)
        sdl2.SDL_RenderPresent(self.renderer)
        sdl2.SDL_DestroyTexture(texture)

    def draw_end(self):
        sdl2.SDL_DestroyRenderer(self.renderer)
        sdl2.SDL_DestroyWindow(self.window)
        sdl2.SDL_Quit()

    ###
    # DRAWING FUNCTIONS
    ###

    def draw_clear(self):
        self.active_draw.rectangle(
            [0, 0, self.screen_width, self.screen_height], fill="black"
        )

    def draw_text(self, position, text, font=15, color="white", **kwargs):
        self.active_draw.text(
            position, text, font=ImageFont.truetype(font_file, font), fill=color, **kwargs
        )

    def draw_rectangle(self, position, fill=None, outline=None, width=1):
        self.active_draw.rectangle(position, fill=fill, outline=outline, width=width)

    def draw_rectangle_r(self, position, radius, fill=None, outline=None):
        self.active_draw.rounded_rectangle(position, radius, fill=fill, outline=outline)

    def draw_circle(self, position, radius, fill=None, outline="white"):
        self.active_draw.ellipse(
            [
                position[0],
                position[1],
                position[0] + radius,
                position[1] + radius,
            ],
            fill=fill,
            outline=outline,
        )

    def draw_log(self, text, fill="Black", outline="black", width=500):
        x = (self.screen_width - width) / 2
        y = (self.screen_height - 80) / 2
        self.draw_rectangle_r([x, y, x + width, y + 80], 5, fill=fill, outline=outline)
        text_x = x + width / 2
        text_y = y + 40
        self.draw_text((text_x, text_y), text, anchor="mm")
