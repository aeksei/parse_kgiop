from unittest import TestCase

from main import extract_tag_kgiop_object,  flat_html


HTML_KGIOP_OBJECT_WITH_COORDS = "kgiop_object_with_coords.html"
HTML_CONTENT_DATA = "layerobject_detail__content__data.html"


class TestClass(TestCase):
    def test_extract_tag_kgiop_object(self) -> None:
        object_id = 1
        with open(HTML_KGIOP_OBJECT_WITH_COORDS) as f:
            html = f.read()

        with open(HTML_CONTENT_DATA) as f:
            content_data = f.read()

        tag = extract_tag_kgiop_object(html, object_id)

        self.assertEqual(content_data, flat_html(str(tag)))

