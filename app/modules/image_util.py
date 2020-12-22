"""
Class containing utilitarian image-based functions intended to reduce
duplicate code.
"""
from os import listdir
from PIL import Image, ImageFont, ImageDraw, ImageColor


async def paste_on_backgrounds(name, overlay) -> bool:
    try:
        for background_file in listdir("assets/images/backgrounds"):
            with Image.open(f"assets/images/backgrounds/{background_file}") as background:
                background = background.resize(
                    (int(overlay.width), int(overlay.height)), Image.ANTIALIAS)
                background.paste(overlay, (0, 0), overlay)
                background.save(
                    f"contents/{background_file[0:3]}{name}.png")
        return True
    except:
        return False


def resize_ratio(image: Image.Image, max_width: int, max_height: int):
    """Resize and return the provided image while maintaining aspect ratio."""
    ratio = max(max_width / image.width, max_height / image.height)
    return image.resize(
        (int(image.width * ratio), int(image.height * ratio)),
        Image.ANTIALIAS
    )


def align_center(background_width: int, foreground_width: int, distance_top: int = 0):
    """Return the tuple necessary for horizontal centering and an optional vertical distance."""
    return background_width // 2 - foreground_width // 2, distance_top


def get_font(size: int):
    """
    :size -> font size of text
    :return -> A font object with the specified font file and size.
    """
    return ImageFont.truetype("assets/fonts/BurbankBigCondensed-Black.ttf", size)


def get_tools(card_size: tuple) -> tuple:
    """
    Makes image and calling an object
    There isn't anything special and it used only for
    reducing duplicate code btw :/ <3

    Args:
        card_size (tuple): width and height of card

    Returns:
        tuple: raw image and canvas to draw text
    """
    card = Image.new("RGBA", card_size)
    canvas = ImageDraw.Draw(card)
    return card, canvas


def hex_to_rgb(hex_code: str) -> tuple:
    """
    Converts HTML color code to RGB Color

    :hex_code -> html color code
    """
    return ImageColor.getcolor(hex_code, "RGBA")


def fit_text(text: str, size: int, max_size: int):
    """
    Return the font and width which fits the provided text within the
    specified maxiumum width.

    :text -> string text that we want to fit it
    :size -> main font size of text
    :max_size -> max width size per pixel
    :return -> font object + new text width + change int to align the text
    """
    font = get_font(size)
    text_width, _ = font.getsize(text)
    change = 0

    while text_width >= max_size:
        change += 1
        size -= 1
        font = get_font(size)
        text_width, _ = font.getsize(text)

    return font, text_width, change
