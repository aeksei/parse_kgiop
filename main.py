import json
import asyncio
from typing import Optional
from random import randint

import httpx

import kgiop_parser
from logger_config import get_logger


logger = get_logger(__name__)

HTTPX_CONNECT_TIMEOUT = None
BASE_URL = "https://kgiop.gov.spb.ru/uchet/list_objects/"
OUTPUT_FILE = "kgiop_objects.json"


async def main():
    objects_list = await get_all_kgiop_objects()
    to_json(objects_list)


async def get_kgiop_object(a_client, object_id: int) -> Optional[dict]:
    url = f"{BASE_URL}{object_id}/"

    logger.debug(f"Object {object_id} try loading started...")
    response = await a_client.get(url, timeout=HTTPX_CONNECT_TIMEOUT)

    if response.status_code == httpx.codes.OK:
        logger.info(f"Object {object_id} successful load")
        return parse_kgiop_object(response.text, object_id)
    elif response.status_code == httpx.codes.NOT_FOUND:
        logger.error(f"Page {url} not found")
        return None
    elif response.status_code == httpx.codes.SERVICE_UNAVAILABLE:
        await asyncio.sleep(randint(5, 60))
        return await get_kgiop_object(a_client, object_id)  # recursion
    else:
        logger.critical(response)  # unknown error


async def get_all_kgiop_objects(start_id: int = 1, end_id: int = 9670):
    logger.info("Start load all objects")
    async with httpx.AsyncClient() as a_client:
        tasks = [get_kgiop_object(a_client, object_id) for object_id in range(start_id, end_id)]
        objects_list = await asyncio.gather(*tasks)

    logger.info("End load all objects")
    return objects_list



def to_json(objects_list):
    objects_list = sorted(objects_list, key=lambda item: item["id"])
    with open(OUTPUT_FILE, "w") as f:
        json.dump(objects_list, f, indent=4)


def parse_kgiop_object(html: str, object_id: int) -> Optional[dict]:
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


if __name__ == '__main__':
    asyncio.run(main())
