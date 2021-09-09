import re
import asyncio
import logging
from typing import Optional
from random import randint

import httpx
from bs4.element import Tag
from bs4 import BeautifulSoup

BASE_URL = "https://kgiop.gov.spb.ru/uchet/list_objects/"
COORDS_PATTERN = re.compile(r"coords = \[.*?'\];")
LAT_LON_PATTERN = re.compile(r"coords = \['(?P<lat>-?\d{1,2}\.\d*?\s*?)', '(?P<lon>-?\d{1,3}\.\d*?\s*?)'\];")  # lat lon


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
consoleHandler.setFormatter(formatter)

# add ch to logger
logger.addHandler(consoleHandler)


async def main():
    tasks = [get_kgiop_object(object_id) for object_id in range(1, 100)]
    return await asyncio.gather(*tasks)


async def get_kgiop_object(object_id: int) -> Optional[dict]:
    url = f"{BASE_URL}{object_id}/"

    logger.info(f"Object {object_id} loading started...")
    async with httpx.AsyncClient() as a_client:
        await asyncio.sleep(randint(1, 10))
        response = await a_client.get(url)

    if response.status_code == httpx.codes.NOT_FOUND:
        logger.error(f"Page {url} not found")
        return None
    elif response.status_code == httpx.codes.OK:
        html = response.text

        tag = extract_tag_kgiop_object(html, object_id)
        if not tag:
            logger.error(f"Object {object_id} not parsed.")
            return None
        else:
            kgiop_dict = get_kgiop_dict(tag)
            coords = extract_coords(html, object_id)
            kgiop_dict["coords"] = coords
            kgiop_dict["id"] = object_id
            logger.info(f"Object {object_id} successful load.")
            return kgiop_dict
    else:
        logger.error(response)


def extract_tag_kgiop_object(html: str, object_id: int) -> Optional[Tag]:
    tag_name = "div"
    class_ = "layerobject_detail__content__data"

    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find(tag_name, class_=class_)

    if tag is None:
        logger.error(f"Tag {tag_name} class {class_} not found for object {object_id}")
    else:
        html = str(tag)
        logger.debug(f"Object {object_id} {flat_html(html)}")

    return tag


def get_kgiop_dict(tag: Tag) -> dict:
    key_class = "layerobject_detail__content__data__key"
    value_class = "layerobject_detail__content__data__value"

    keys = [key_tag.get_text(strip=True) for key_tag in tag.find_all("span", class_=key_class)]
    values = [value_tag.get_text(strip=True) for value_tag in tag.find_all("span", class_=value_class)]

    return dict(zip(keys, values))


def extract_coords(html: str, object_id: int) -> Optional[dict]:
    coords = COORDS_PATTERN.search(html)
    if not coords:
        logger.warning(f"Parsed coords not found on page for object {object_id}.")
    else:
        coords = coords.group(0)
        logger.debug(f"Object {object_id} {coords}")

        lat_lon = LAT_LON_PATTERN.search(coords)
        if not lat_lon:
            logger.warning(f"Coords found for object {object_id} but not parsed.")
        else:
            return lat_lon.groupdict()


def flat_html(html: str) -> str:
    return "".join(line.strip() for line in html.split("\n"))


if __name__ == '__main__':
    print(asyncio.run(main()))
    # asyncio.run(get_kgiop_object(38))
