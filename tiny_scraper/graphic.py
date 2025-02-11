from fcntl import ioctl
from PIL import Image, ImageDraw, ImageFont
from main import hw_info
import mmap
import os

fb: int
mm: mmap.mmap

screen_resolutions = {
    1: (720, 720),
    2: (720, 480),
}

screen_width, screen_height = screen_resolutions.get(hw_info, (640, 480))
bytes_per_pixel = 4
screen_size = screen_width * screen_height * bytes_per_pixel
fb_screeninfo = None

fontFile = {}
fontFile[17] = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSansMono.ttf", 17)
fontFile[15] = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSansMono.ttf", 15)
fontFile[13] = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSansMono.ttf", 13)
fontFile[11] = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSansMono.ttf", 11)
colorBlue = "#bb7200"
colorBlueD1 = "#7f4f00"
colorGray = "#292929"
colorGrayL1 = "#383838"
colorGrayD2 = "#141414"

activeImage: Image.Image
activeDraw: ImageDraw.ImageDraw


def get_fb_screeninfo():
    global fb_screeninfo
    if hw_info == 3:
        fb_screeninfo = b'\xe0\x01\x00\x00\x80\x02\x00\x00\xe0\x01\x00\x00\x80\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x18\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00^\x00\x00\x00\x96\x00\x00\x00\x00\x00\x00\x00\xc2\xa2\x00\x00\x1a\x00\x00\x00T\x00\x00\x00\x0c\x00\x00\x00\x1e\x00\x00\x00\x14\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    else:
        fb_fd = os.open("/dev/fb0", os.O_RDWR)
        try:
            fb_info = bytearray(160)
            ioctl(fb_fd, 0x4600, fb_info)
            fb_screeninfo = bytes(fb_info)
        finally:
            #print(fb_screeninfo)
            os.close(fb_fd)
    return fb_screeninfo

def screen_reset():
    ioctl(
        fb,
        0x4601,
        fb_screeninfo,
    )
    ioctl(fb, 0x4611, 0)


def draw_start():
    global fb, mm
    fb = os.open("/dev/fb0", os.O_RDWR)
    mm = mmap.mmap(fb, screen_size)


def draw_end():
    global fb, mm
    mm.close()
    os.close(fb)


def create_image():
    image = Image.new("RGBA", (screen_width, screen_height), color="black")
    return image


def draw_active(image):
    global activeImage, activeDraw
    activeImage = image
    activeDraw = ImageDraw.Draw(activeImage)


def draw_paint():
    global activeImage
    if hw_info == 3:
        img = activeImage.rotate(90, expand=True)
        mm.seek(0)
        mm.write(img.tobytes())
    else:
        mm.seek(0)
        mm.write(activeImage.tobytes())


def draw_clear():
    global activeDraw
    activeDraw.rectangle((0, 0, screen_width, screen_height), fill="black")


def draw_text(position, text, font=15, color="white", **kwargs):
    global activeDraw
    activeDraw.text(position, text, font=fontFile[font], fill=color, **kwargs)


def draw_rectangle(position, fill=None, outline=None, width=1):
    global activeDraw
    activeDraw.rectangle(position, fill=fill, outline=outline, width=width)


def draw_rectangle_r(position, radius, fill=None, outline=None):
    global activeDraw
    activeDraw.rounded_rectangle(position, radius, fill=fill, outline=outline)


def draw_circle(position, radius, fill=None, outline="white"):
    global activeDraw
    activeDraw.ellipse(
        [position[0], position[1], position[0] + radius, position[1] + radius],
        fill=fill,
        outline=outline,
    )


def draw_log(text, fill="Black", outline="black", width=500):
    # Center the rectangle horizontally
    x = (screen_width - width) / 2
    # Center the rectangle vertically
    y = (screen_height - 80) / 2  # 80 is the height of the rectangle
    draw_rectangle_r([x, y, x + width, y + 80], 5, fill=fill, outline=outline)

    # Center the text within the rectangle
    text_x = x + width / 2
    text_y = y + 40  # Vertically center within the 80px height
    draw_text((text_x, text_y), text, anchor="mm")  # Use middle-middle anchor


fb_screeninfo = get_fb_screeninfo()

draw_start()
screen_reset()

imgMain = create_image()
draw_active(imgMain)
