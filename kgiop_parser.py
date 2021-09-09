import re
import logging
from typing import Optional

from bs4.element import Tag
from bs4 import BeautifulSoup

COORDS_PATTERN = re.compile(r"coords = \[.*?'\];")
LAT_LON_PATTERN = re.compile(r"coords = \['(?P<lat>\s*?-?\d{1,2}\.\d*?\s*?)', '(?P<lon>\s*?-?\d{1,3}\.\d*?\s*?)'\];")  # lat lon

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