"""Track changes of LlamaShop Features"""
import os
import json
from asyncio import create_task, sleep
from app.modules.request import get_url
from app.modules.json_creator import save_itemshop_json, save_news_json
from .image_generators import generate_itemshop, generate_news


class FortiteAPI:
    """Fortnite API Tracker class"""
    hashes = {"itemshop": "", "brnews": "", "creativenews": "", "stwnews": ""}

    async def track_hashes(self, base_info: tuple, its_news: bool) -> dict:
        """
        Gets feature_data (name + url of item) then check hash diffrence
        between old saved hash and new hash, if there was any diffrence, it
        returns dict with some content else it returns empty dict
        """
        final_content = {}
        url, game_modes = base_info
        raw_data = await get_url(url)

        try:
            if raw_data["status"] == 200 and raw_data["data"] is not None:
                for mode in game_modes:
                    data = raw_data["data"]
                    data = data[mode[:-4]] if its_news else data

                    if (data["hash"] == self.hashes[mode]) is False:
                        self.hashes[mode] = data["hash"]
                        final_content[mode] = data
        except Exception:
            pass

        return final_content

    async def track_itemshop(self) -> None:
        """
        Track chnages of itemshop
        """
        url = "https://fortnite-api.com/v2/shop/br/combined"
        game_mode = ["itemshop"]

        while True:
            data = await self.track_hashes((url, game_mode), False)
            if len(data.keys()) != 0:
                mode_data = data["itemshop"]
                if await generate_itemshop(mode_data):
                    await save_itemshop_json(mode_data)

            await sleep(10)

    async def track_news(self) -> None:
        """
        Track chnages of NewsPage
        """
        url = "https://fortnite-api.com/v2/news"
        game_modes = ["brnews", "creativenews", "stwnews"]

        while True:
            data = await self.track_hashes((url, game_modes), True)
            if len(data.keys()) != 0:
                for mode in game_modes:
                    if mode in data:
                        if await generate_news(data[mode], mode):
                            await save_news_json(mode, data[mode])
            await sleep(10)
