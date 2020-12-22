"""
Modules to have a nice & sucessful HTTP request + return
"""
import io
import aiohttp


async def get_url(url: str, params: dict = None, headers: dict = None) -> dict:
    """
    HTTP request to the url the returns json decoded data

    :url -> url of the API
    :params -> parameters, anything
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as resp:
            return await resp.json()


async def get_url_file(url):
    """
    Open and read bytes of the file from url

    :url -> url of the file
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            img = await resp.content.read()
            return io.BytesIO(img) if resp.status == 200 else None


async def download_file(url, file_name) -> bool:
    """
    Download a file to a specified path

    :url -> url of the file
    :file_name -> file path and name with extension of that
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            with open(f'contents/{file_name}', mode='wb') as byte_file:
                byte_file.write(await resp.read())
            return resp.status == 200
