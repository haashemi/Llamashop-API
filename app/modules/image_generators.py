from math import ceil
from textwrap import wrap
from .calendar import get_time, get_delta_time
from .request import get_url, get_url_file
from .image_util import get_tools, get_font, paste_on_backgrounds, \
    Image, resize_ratio, align_center, fit_text


class CardCreator:

    @staticmethod
    async def create_shop_card(item: dict):
        """
        Generates the image of item for Itemshop/Leaks

        Args:
            item (dict): Raw data of that item which collected
            from fortnite-api.com/v2/shop/br/combined

        Returns:
            class 'PIL.Image.Image': Generated image card
        """
        try:
            name = item["items"][0]["name"]
            rarity = item["items"][0]["rarity"]["value"]
            history = item["items"][0]["shopHistory"]
            price = item["finalPrice"]

            if item["items"][0]["images"]["featured"] is not None:
                icon = item["items"][0]["images"]["featured"]
            else:
                icon = item["items"][0]["images"]["icon"]
        except KeyError:
            return

        # ________________________________________
        #    MAKKE IMAGE + PASTE RAIRITY LAYER
        card, canvas = get_tools((300, 350))

        try:
            bacground = Image.open(
                f"./assets/images/Modern/Background_{rarity}.png")
        except FileNotFoundError:
            bacground = Image.open(
                "./assets/images/Modern/Background_common.png")
        card.paste(bacground, (0, 0), bacground)

        # ________________________________________
        #      DOWNLOAD & PASTE ICON ON LAYER
        icon = Image.open(await get_url_file(icon)).convert("RGBA")
        icon = resize_ratio(icon, 300, 300)
        card.paste(icon, align_center(
            card.width, icon.width, 15), icon)
        # ________________________________________
        #             PASTE OVERLAYS
        try:
            layer = Image.open(
                f"./assets/images/Modern/Overlay_{rarity}.png")
        except FileNotFoundError:
            layer = Image.open(
                "./assets/images/Modern/Overlay_common.png")

        card.paste(
            layer,
            (0, card.height - layer.height),
            layer
        )
        # ________________________________________
        #           Draw name & price

        font = get_font(33)
        text_width, _ = font.getsize(name)
        change = 0
        if text_width >= 300:
            font, text_width, change = fit_text(name, 33, 300)
        canvas.text(
            align_center(
                card.width,
                text_width,
                (285 + (change // 2))
            ),
            name,
            font=font
        )

        font = get_font(26)
        price = str(f"{price:,}")
        text_width, _ = font.getsize(price)
        canvas.text(
            (card.width - text_width - 45, card.height - 25),
            price,
            font=font
        )

        font = get_font(20)
        if len(history) <= 1:
            history_text = "NEW ITEM"
        elif len(history) > 1:
            last_seen = f"{get_delta_time(history[-2])} AGO".upper()
            history_text = f"{len(history)} Times | {last_seen}"
        else:
            return

        # >>>> DRAW HISTORY TEXT <<<<
        text_width, _ = font.getsize(history_text)
        change = 0
        if text_width >= 175:
            font, text_width, change = fit_text(history_text, 20, 175)
        canvas.text(
            (5, card.height - 23),
            history_text,
            fill=(185, 203, 209),
            font=font
        )

        # ________________________________________
        #          DONE! NOW RETURN IT
        return card

    @staticmethod
    async def create_news_card(news: dict):
        """
        Generates the image of item for news page

        Args:
            item (dict): Raw data of that item which collected
            from fortnite-api.com

        Returns:
            class 'PIL.Image.Image': Generated image card
        """
        # ___________________________________________________
        #                  COLLECT DATA
        try:
            title = news["title"]
            description = news["body"]
            image = news["image"]
        except KeyError:
            return

        card, canvas = get_tools((900, 750))
        # ___________________________________________________
        #              PASTE NEWS IMAGE ON CARD
        icon = Image.open(await get_url_file(image)).convert("RGBA")
        icon = resize_ratio(icon, 900, 506)
        card.paste(icon, (0, 0), icon)
        # ___________________________________________________
        #                PASTE IMAGE OVERLAY
        layer = Image.open("assets/images/NewsCard.png")
        card.paste(layer, (0, card.height - layer.height), layer)
        # ___________________________________________________
        #               DRAW TITLE ON OVERLAY
        font = get_font(75)
        text_width, _ = font.getsize(title)
        change = 0
        if text_width >= 900:
            font, text_width, change = fit_text(title, 30, 870)
        canvas.text(
            (20, 470 + (change // 2)),
            title,
            fill=(0, 0, 0),
            font=font
        )
        # ___________________________________________________
        #            DRAW DESCRIPTION ON OVERLAY
        font = get_font(40)
        margin = 0
        for margin, line in enumerate(wrap(description, width=60, max_lines=3)):
            text_width, _ = font.getsize(line)
            canvas.text(
                (30, 600 + (margin * 45)),
                line,
                font=font
            )
            margin += 45
        # ___________________________________________________
        #               DONE! RETURN THE CARD
        return card


async def generate_itemshop(data: dict) -> bool:
    """Generates itemshop image and save them somewhere

    Args:
        data (dict): raw collected data from fortnite-api

    Returns:
        bool: Status of saving image (True = Saved | False = Error)
    """
    featured = data["featured"]["entries"]
    daily = data["daily"]["entries"]

    rows = max(ceil((len(featured) / 3)), ceil((len(daily) / 3)))

    shop_image, canvas = get_tools((2000, ((355 * rows) + 480)))

    font = get_font(100)
    canvas.text((355, 255), "Featured", font=font)
    canvas.text((1397, 255), "Daily", font=font)

    canvas.text(
        (0, shop_image.height - 30),
        "Provided by LlamaShop.ir",
        font=(get_font(25))
    )

    for i, item in enumerate(featured):
        card = await CardCreator.create_shop_card(item)
        if card is not None:
            shop_image.paste(
                card,
                (
                    (60 + ((i % 3) * (card.width + 5))),
                    (365 + ((i // 3) * (card.height + 5)))
                ),
                card
            )

    for i, item in enumerate(daily):
        card = await CardCreator.create_shop_card(item)
        if card is not None:
            shop_image.paste(
                card,
                (
                    (1030 + ((i % 3) * (card.width + 5))),
                    (365 + ((i // 3) * (card.height + 5)))
                ),
                card
            )

    return await paste_on_backgrounds("itemshop", shop_image)


async def generate_news(item: dict, mode) -> bool:
    """Generates news page image and save them somewhere

    Args:
        data (dict): raw collected data from fortnite-api

    Returns:
        bool: Status of saving image (True = Saved | False = Error)
    """
    # >>>> COLLECT DATA <<<<
    items = item["messages"] if item["motds"] is None else item["motds"]

    # >>>> MAKE IMAGE <<<<
    items_count = len(items)
    columns = 3 if items_count > 3 else items_count
    news_image, canvas = get_tools(
        (
            ((columns - 1) * 40) + (columns * 900) + 80,
            (750 * ceil(items_count / 3)) + 440
        )
    )

    # >>>> DRAW "NEWS" TOP,CENTER OF IMAGE <<<<
    font = get_font(250)
    text_width, _ = font.getsize("News")
    canvas.text(((news_image.width - text_width) // 2, 70),
                "News", font=font)

    # >>>> GENERATE CARD OF NEWS AND PASTE ON MAIN IMAGE <<<<
    for i, news in enumerate(items):
        card = await CardCreator.create_news_card(news)
        if card is not None:
            news_image.paste(
                card,
                (
                    (40 + ((i % 3) * (card.width + 40))),
                    (350 + ((i // 3) * (card.height + 20)))
                ),
                card
            )

    # >>>> SAVE IMAGE <<<<
    return await paste_on_backgrounds(mode, news_image)
