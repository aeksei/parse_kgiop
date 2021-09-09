import asyncio
from typing import Optional
from random import randint

import httpx

import kgiop_parser
from logger_config import get_logger


logger = get_logger(__name__)

HTTPX_CONNECT_TIMEOUT = None
BASE_URL = "https://kgiop.gov.spb.ru/uchet/list_objects/"


async def main():
    tasks = [get_kgiop_object(object_id) for object_id in range(1, 10)]
    return await asyncio.gather(*tasks)


async def get_kgiop_object(object_id: int) -> Optional[dict]:
    url = f"{BASE_URL}{object_id}/"

    logger.debug(f"Object {object_id} try loading started...")
    async with httpx.AsyncClient() as a_client:
        response = await a_client.get(url, timeout=HTTPX_CONNECT_TIMEOUT)

    if response.status_code == httpx.codes.NOT_FOUND:
        logger.error(f"Page {url} not found")
        return None
    elif response.status_code == httpx.codes.OK:
        logger.info(f"Object {object_id} successful load")
        html = response.text

        tag = kgiop_parser.extract_tag_kgiop_object(html, object_id)
        if not tag:
            logger.error(f"Object {object_id} not parsed.")
            return None
        else:
            kgiop_dict = kgiop_parser.get_kgiop_dict(tag)
            coords = kgiop_parser.extract_coords(html, object_id)
            kgiop_dict["coords"] = coords
            kgiop_dict["id"] = object_id
            return kgiop_dict
    elif response.status_code == httpx.codes.SERVICE_UNAVAILABLE:
        await asyncio.sleep(randint(5, 60))
        return await get_kgiop_object(object_id)  # recursion
    else:
        logger.critical(response)  # unknown error


if __name__ == '__main__':
    print(asyncio.run(main()))
