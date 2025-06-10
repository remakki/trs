import aiofiles
import aiohttp

from src.config import settings


async def get_video_from_flow(start_time: int, end_time: int) -> str:
    dur = end_time - start_time
    ENDPOINT = settings.REQUEST_URL + f'/archive-{start_time}-{dur}.mp4?token={settings.TOKEN}'
    save_path = f"data/{start_time}-{dur}.mp4"

    async with aiohttp.ClientSession() as session:
        async with session.get(ENDPOINT) as response:
            response.raise_for_status()
            async with aiofiles.open(save_path, "wb") as f:
                while chunk := await response.content.read(1024 * 1024):
                    await f.write(chunk)

    return save_path
