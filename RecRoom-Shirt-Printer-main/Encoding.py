"""
Converts a PNG image into strings of predefined length
How is it encoded:
    the number in front of a char represents how many pixels of the same color are in a row,
    chars !#$%&()*+,./:;<=>?@[Ñ]^_{|}~¢£¤¥¦§¨©ª«¬Ö®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÈÌÐ represent the color.
    There's 62 colors including eraser and tan, eraser is not recommended as it leaves an edge
"""
import os
import subprocess
import sys
import time
import tkinter
from math import sqrt
from pathlib import Path
from tkinter import filedialog
from typing import Tuple, List

try:
    import pyautogui
    import pyperclip
    from PIL import Image, ImageGrab
except ModuleNotFoundError:
    print(f'Please execute the following line and run the script again:\n'
          f'{sys.executable} -m pip install -U PyAutoGUI pyperclip Pillow')
    # Ask the user to install all the necessary packages automatically
    if input("Proceed to run the command automatically? [yes/no] ").find("yes") != -1:
        subprocess.call(f"{sys.executable} -m pip install -U PyAutoGUI pyperclip Pillow")
    exit()

MaxStringLength: int = 512  # Maximum length string

# Typing alias for color
PixelColor = Tuple[int, int, int]

# All of RecRoom color in order + tan marker + eraser
RR_PALETTE: dict = {(101, 113, 149): "!",
(147, 152, 173): "#",
(154, 171, 207): "$",
(84, 88, 107): "%",
(28, 43, 94): "&",
(117, 137, 171): "(",
(38, 96, 154): ")",
(206, 214, 227): "*",
(25, 151, 161): "+",
(163, 202, 211): ",",
(51, 65, 103): ".",
(29, 30, 43): "/",
(112, 148, 193): ":",
(122, 201, 199): ";",
(29, 61, 138): "<",
(77, 51, 25): "=",
(108, 75, 33): ">",
(96, 192, 190): "?",
(192, 190, 191): "@",
(128, 127, 139): "[",
(43, 75, 148): "Ñ",
(0, 0, 0): "]",
(38, 68, 138): "^",
(35, 54, 119): "_",
(50, 83, 155): "{",
(46, 80, 154): "|",
(43, 51, 85): "}",
(34, 43, 73): "~",
(54, 91, 163): "¢",
(36, 61, 130): "£",
(29, 38, 69): "¤",
(28, 44, 105): "¥",
(38, 53, 104): "¦",
(59, 98, 169): "§",
(49, 56, 91): "¨",
(234, 237, 243): "©",
(49, 76, 147): "ª",
(36, 45, 83): "«",
(29, 51, 116): "¬",
(27, 41, 87): "Ö",
(50, 73, 137): "®",
(235, 240, 246): "¯",
(52, 60, 98): "°",
(26, 34, 61): "±",
(29, 48, 108): "²",
(233, 235, 236): "³",
(44, 66, 121): "´",
(50, 69, 121): "µ",
(67, 102, 169): "¶",
(18, 28, 56): "·",
(66, 107, 178): "¸",
(55, 65, 103): "¹",
(32, 46, 103): "º",
(28, 60, 131): "»",
(242, 242, 244): "¼",
(241, 240, 237): "½",
(40, 48, 78): "¾",
(29, 46, 112): "¿",
(56, 81, 139): "À",
(1, 165, 154): "È",
(200, 200, 201): "ß",
(219, 229, 245): "Ä",
(213, 218, 232): "ê",
(201, 212, 233): "ö",
(184, 199, 227): "Ø",
(8, 10, 25): "Ð",
(68, 92, 150): "Ý",
(19, 28, 70): "ä",
(167, 183, 215): "î",
(237, 241, 237): "Œ",
(90, 116, 168): "Ç",
(29, 65, 136): "Ž",
(14, 24, 52): "ÿ",
(240, 238, 244): "Ú",
(184, 196, 218): "É",
(152, 167, 201): "Ê",
(220, 226, 234): "Æ",
(198, 202, 215): "Ë",
(13, 19, 41): "Ù",
(18, 22, 40): "Ü",
(116, 137, 183): "a",
(71, 98, 155): "ƒ",
(102, 121, 168): "ñ",
(62, 104, 177): "å",
(106, 132, 182): "Å",
(134, 155, 197): "ë",
(135, 149, 185): "Ï",
(86, 104, 153): "ï",
(32, 46, 113): "ù",
(70, 87, 137): "ý",
(68, 72, 102): "Ã",
(181, 185, 199): "Â",
(211, 220, 242): "ž",
(28, 68, 148): "Á",
(122, 147, 194): "Ò",
(195, 205, 229): "Ì",
(86, 90, 117): "Í",
(165, 169, 183): "Ó",
(151, 171, 210): "Ô",
(71, 113, 183): "Õ",
(241, 238, 236): "€",
(13, 16, 28): "Š",
(84, 109, 164): "†",
(180, 188, 213): "‡",
(169, 179, 202): "™",
(9, 11, 36): "š",
(148, 152, 169): "œ",
}

# All the RecRoom colors in one list. [R, G, B, R, G, B,...]
ALL_COLORS = [num for tup in RR_PALETTE.keys() for num in tup]


def get_image(check_palette: bool = True) -> Image:
    """
    Open file explorer, wait for user to open a PNG image
    :return: The image
    """
    print("Open image", end="\r")
    root = tkinter.Tk()
    root.attributes("-topmost", 1)
    root.withdraw()
    img_path = filedialog.askopenfilename(filetypes=[("Image", "*.png")])
    root.destroy()

    img = None
    if img_path:
        img = Image.open(img_path)

    if check_palette:
        # If the image has attributed `palette` its metadata is a bit different.
        # To solve this just open the image in paint and save it
        if img.palette:
            print("Image has `Palette` attribute. Open it in Paint and save.")
            os.system(f'mspaint.exe "{Path(img_path)}"')
            return None

    return img


def closest_color(pixel_color: PixelColor) -> PixelColor:
    """
    Take an RGB value and find the closest color in `RR_PALETTE`

    It is recommended you use external programs to convert and dither images.
    2 ACO (swatch) files are included if you're using Photoshop

    :param pixel_color: The color of the pixel of the image
    :return: The color from `RR_PALETTE` that is closest to `pixel_color`
    """
    r, g, b = pixel_color
    color_diffs: List[tuple[float, PixelColor]] = []
    for key in RR_PALETTE:
        cr, cg, cb = key
        color_diff = sqrt((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2)
        color_diffs.append((color_diff, key))
    return min(color_diffs)[1]


def progress_update(y: int, img: Image, prefix='Progress', suffix='', length=50) -> None:
    """
    Display a progress bar in the console
    :param y: The `y` value of the image
    :param img: The image
    :param prefix: Optional: Text in-front of the progress bar
    :param suffix: Optional: Text behind the progress bar
    :param length: Optional: The length of the progress bar
    """
    completed = int(length * y // img.height)
    empty = length - completed
    bar = "#" * completed + " " * empty
    percent = f"{100 * (y / float(img.height)):.2f}"
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end="\r")

    # Print New Line on Complete
    if y == img.height:
        print(" " * (length + 30), end="\r")


def quantize(img, ask_for_dither: bool = True, dither: int = 0, open_image: bool = True) -> Image:
    img = img.convert("RGB")

    if ask_for_dither:
        dither = 0 if "n" in input("Dither the image? [y/n] ").lower() else 1

    palette_image = Image.new("P", img.size)
    palette_image.putpalette(ALL_COLORS)
    new_image = img.quantize(palette=palette_image,
                             dither=dither).convert("RGB")

    if open_image:
        print("Opening the final image...")
        new_image.show()

    return new_image


def encode(img: Image, vertical_print: bool = False, dither_: bool = True) -> list[str] or None:
    """
    Take an image and encode it into a list of {`MaxStringLength`}-char strings.
    ...[number of pixels][color]...

    :param img: The image to be encoded.
    :param vertical_print: Encode the image vertically (for Ashers printer)
    :param dither_: Should the image be dithered
    :return: List of {`MaxStringLength`} char long strings
    """
    pixel_color: List[str] = []
    full_image = Image.new("RGB", img.size)
    dither = False

    # Just so pycharm doesn't complain
    x, y = 0, 0

    if dither_:
        img = quantize(img)

    # `vertical_print` just changes the orientation of the encoding process.
    for y in range(img.height):
        for x in range(img.width):
            p = img.getpixel((y, x) if vertical_print else (x, y))  # Gets the color of the pixel at `x, y`
            if len(p) == 4:  # If the value is RGBA, the last `int` is removed
                p = p[:3]
            try:
                # Check if the image has already been dithered, else find the closest color
                p = RR_PALETTE[p]
            except KeyError:
                dither = True
                p = closest_color(p)
                full_image.putpixel((y, x) if vertical_print else (x, y), p)
                p = RR_PALETTE[p]
                # closest_color(p)
            pixel_color.append(p)
        # Print the progress
        progress_update(y + 1, img, "Encoding")

    if dither and dither_:
        full_image.show()

    colors: List[Tuple[int, str]] = []
    count: int = 0
    current_color: str = pixel_color[0]
    # `count` is the amount of `current_color` in a row

    for c in pixel_color:
        if c != current_color:
            colors.append((count, current_color))
            count = 0
            current_color = c
        count += 1
    colors.append((count, current_color))

    print(f"Compressed {len(pixel_color)} chars into {len(colors)} chars")

    s: str = ""
    img_data: List[str] = []
    for amount, color in colors:
        if amount > 1:
            ns = f"{amount}{color}"
        else:
            ns = color

        if len(s + ns) > MaxStringLength:  # 512
            img_data.append(s)
            s = ""
        s += ns

    img_data.append(s)
    return img_data


def main(list_size: int, output_strings: bool = False, wait_for_input: bool = False):
    """
    Function to tie together all others.
    Prompt for image, encode and output

    :param list_size: The max list size; 50 for `Variable` importing, 64 for `List Create` importing
    :param output_strings: Print the encoded image strings into the console
    :param wait_for_input: Wait for the user to continue. Useful when running this file directly so that it stays open
    """

    img: Image = get_image()
    if not img:
        exit()

    img_data: list[str] = encode(img)

    with open("image_data.txt", "w", encoding="UTF-8") as strings_file:
        strings_file.writelines("\n".join(img_data))

    if output_strings:
        print("Copying strings\n_______________\n")
        time.sleep(2)
        # Print all image data strings
        print("\n\n".join(img_data))

    # Print amount of {`MaxStringLength`} char long strings, image dimensions and total `List Create`s needed.
    print(f"\nGenerated {len(img_data) + 2} strings for image WxH {img.width}x{img.height}")
    print(f"Space needed: {len(img_data) // list_size} Lists (+ {len(img_data) % list_size})")

    if wait_for_input:
        input("Press enter to continue")

    return img, img_data


if __name__ == '__main__':
    try:
        main(output_strings=True,
             wait_for_input=True,
             list_size=50 if "1" in input("1. Variable Import\n2. List Create Import\n> ") else 64)
    except KeyboardInterrupt:
        pass
