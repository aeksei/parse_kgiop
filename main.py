import re
import asyncio
import logging
from typing import Optional

import httpx
from bs4.element import Tag
from bs4 import BeautifulSoup

BASE_URL = "https://kgiop.gov.spb.ru/uchet/list_objects/"
COORDS_PATTERN = re.compile(r"coords = \[.*?'\];")
LAT_LON_PATTERN = re.compile(r"coords = \['(?P<lat>-?\d{1,2}\.\d{,6})', '(?P<lon>-?\d{1,3}\.\d{,6})'\];")  # lat lon


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


async def get_kgiop_object(object_id: int) -> Optional[dict]:
    url = f"{BASE_URL}{object_id}/"

    logger.info(f"Start load object {object_id}")
    async with httpx.AsyncClient() as a_client:
        response = await a_client.get(url)
    html = response.text

    tag = extract_tag_kgiop_object(html, object_id)
    kgiop_dict = get_kgiop_dict(tag)

    coords = extract_coords(html, object_id)


def extract_tag_kgiop_object(html: str, object_id: int) -> Optional[Tag]:
    tag = "div"
    class_ = "layerobject_detail__content__data"

    soup = BeautifulSoup(html, "html.parser")
    data = soup.find(tag, class_=class_)

    if data is None:
        logger.error(f"Для объекта {object_id} данные не найдены.")
    else:
        html = str(data)
        logger.debug(flat_html(html))

    return data


def get_kgiop_dict(tag: Tag) -> dict:
    key_class = "layerobject_detail__content__data__key"
    value_class = "layerobject_detail__content__data__value"

    keys = [key_tag.string for key_tag in tag.find_all("span", class_=key_class)]
    values = [value_tag.string for value_tag in tag.find_all("span", class_=value_class)]

    return dict(zip(keys, values))


def extract_coords(html: str, object_id: int) -> Optional[dict]:
    coords = COORDS_PATTERN.search(html)
    if not coords:
        logger.warning(f"Объект {object_id} не имеет координат.")
    else:
        coords = coords.group(0)
        logger.debug(coords)

        lat_lon = LAT_LON_PATTERN.search(coords)
        if not lat_lon:
            logger.warning(f"Координаты для объекта {object_id} были найдены, но не были извлечены.")
        else:
            return lat_lon.groupdict()


def flat_html(html: str) -> str:
    return "".join(line.strip() for line in html.split("\n"))


if __name__ == '__main__':
    print(asyncio.run(get_kgiop_object(1)))
