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


class StatsGenerator:
    """
    Class of everything that needed to make the Stats image
    """

    def __init__(self) -> None:
        """
        Open/Ready necessary things
        """
        self.stats = Image.open("./assets/images/Stats/#file.png")
        self.draw = ImageDraw.Draw(self.stats)
        self.font = ImageFont.truetype(
            r"assets/fonts/BurbankBigCondensed-Black.ttf", 60)

    async def draw_on(self, position: tuple, text, color: tuple = None) -> None:
        """
        Draw some text on specific posotion of image
        :param position: Position of text (x, y)
        :param text: Any text you want to draw on image (int/float/str)
        :param color: RGB Color of text (R, G, B)
        """
        color = color if color is not None else (255, 255, 255)
        self.draw.text(position, str(text), color, self.font)

    async def get_stats(self, username, mode: str, data: dict) -> None:
        """
        Make an Image of player stats, main thing happens here
        :param username: Username of player
        :param mode: Game mode (overall/solo/duo/squad)
        :param data: Collected json data from API
        """
        await self.draw_on((140, 155), data["account"]["name"])
        await self.draw_on((785, 155),
                           str(data["battlePass"]["level"]) + "." + str(data["battlePass"]["progress"]))
        await self.draw_on((140, 400), data["stats"]["all"][mode]["wins"])

        if mode == "overall" or mode == "solo":
            await self.draw_on((590, 310), "10", (243, 239, 255))
            await self.draw_on((535, 400), data["stats"]["all"][mode]["top10"])
            await self.draw_on((990, 310), "25", (243, 239, 255))
            await self.draw_on((930, 400), data["stats"]["all"][mode]["top25"])
        elif mode == "duo":
            await self.draw_on((590, 310), "5", (243, 239, 255))
            await self.draw_on((535, 400), data["stats"]["all"][mode]["top5"])
            await self.draw_on((990, 310), "12", (243, 239, 255))
            await self.draw_on((930, 400), data["stats"]["all"][mode]["top12"])
        elif mode == "squad":
            await self.draw_on((590, 310), "3", (243, 239, 255))
            await self.draw_on((535, 400), data["stats"]["all"][mode]["top3"])
            await self.draw_on((990, 310), "5", (243, 239, 255))
            await self.draw_on((930, 400), data["stats"]["all"][mode]["top6"])

        await self.draw_on((140, 650), data["stats"]["all"][mode]["kills"])
        await self.draw_on((535, 650), data["stats"]["all"][mode]["killsPerMatch"])
        await self.draw_on((930, 650), data["stats"]["all"][mode]["kd"])
        await self.draw_on((140, 905), data["stats"]["all"][mode]["matches"])
        await self.draw_on((930, 905), data["stats"]["all"][mode]["winRate"])
        await self.draw_on((140, 1140), data["stats"]["all"][mode]["minutesPlayed"])
        await self.draw_on((785, 1140), mode.upper())

        self.stats.save(f"./contents/stats/{username}_{mode}.png")
