import unittest

from bs4 import BeautifulSoup

from kgiop_parser import extract_tag_kgiop_object, flat_html, get_kgiop_dict, extract_coords
from kgiop_parser import LAT_LON_PATTERN


class BaseTestCases:
    class TestKgiopObjectBase(unittest.TestCase):
        object_id = None
        KGIOP_DICT = None
        COORDS = None

        @classmethod
        def setUpClass(cls) -> None:
            html_kgiop_object = f"kgiop_object_id_{cls.object_id}.html"
            html_content_data = f"content_data_object_id_{cls.object_id}.html"

            with open(html_kgiop_object) as f:
                cls.html = f.read()

            with open(html_content_data) as f:
                cls.content_data = f.read()

        def test_extract_tag_kgiop_object(self) -> None:
            tag = extract_tag_kgiop_object(self.html, self.object_id)

            self.assertEqual(self.content_data, flat_html(str(tag)))

        def test_get_kgiop_dict(self) -> None:
            tag = extract_tag_kgiop_object(self.html, self.object_id)
            kgiop_dict = get_kgiop_dict(tag)

            self.assertEqual(self.KGIOP_DICT, kgiop_dict)

        def test_extract_coords(self) -> None:
            coords = extract_coords(self.html, self.object_id)
            self.assertEqual(self.COORDS, coords)


class TestKgiopObjectBaseWithCoords(BaseTestCases.TestKgiopObjectBase):
    object_id = 1
    KGIOP_DICT = {
        'Наименование ансамбля': '—',
        'Наименование объекта': 'Здание Консисторского управления Могилевской Римско-католической архиепархии с костелом Успения Девы Марии (Духовная семинария Римско-католической архиепархии)',
        'Время возникновения объекта, основных перестроек': '1870-1873; 1878-1879; 1896-1897; 1900-1902',
        'Местонахождение объекта': '1-я Красноармейская ул., 11, лит. А, Б',
        'Категория историко-культурного значения объекта': 'объект культурного наследия регионального значения',
        'Наименование и реквизиты нормативно-правового акта органа государственной власти о постановке объекта культурного наследия на государственную охрану': 'Распоряжение КГИОП № 10-22 от 21.07.2009',
        'Вид объекта': 'Памятник'
    }
    COORDS = {'lat': '59.916595', 'lon': '30.312194'}


class TestKgiopObjectBaseWithoutCoords(BaseTestCases.TestKgiopObjectBase):
    object_id = 9651
    KGIOP_DICT = {
        'Наименование ансамбля': '—',
        'Наименование объекта': 'Подъездная аллея Свято-Троицкого кладбища',
        'Время возникновения объекта, основных перестроек': '—',
        'Местонахождение объекта': 'г. Петергоф, Свято-Троицкое кладбище, от Нижней дороги до часовни',
        'Категория историко-культурного значения объекта': 'выявленный объект культурного наследия',
        'Наименование и реквизиты нормативно-правового акта органа государственной власти о постановке объекта культурного наследия на государственную охрану': 'Распоряжение КГИОП № 120-р от 09.04.2020',
        'Вид объекта': 'Ансамбль'
    }

    COORDS = None


class TestLatLonPattern(unittest.TestCase):

    def test_lat_lon_pattern(self):
        coords_str_list = [
            "coords = ['59.917676 ', '30.315279'];",
            "coords = ['59.913315', ' 30.298345'];",
            "coords = ['59.9292402709', '30.3178074566'];",
        ]

        for coords in coords_str_list:
            with self.subTest(coords=coords):
                self.assertIsNotNone(LAT_LON_PATTERN.search(coords))


class TestGetKgiopDict(unittest.TestCase):

    def test_whitespace_around_get_text(self):
        # object_id = 2
        content_data = """<div class="layerobject_detail__content__data"><span class="layerobject_detail__content__data__key">Наименование ансамбля</span><span class="layerobject_detail__content__data__value layerobject_detail__content__data--text">—</span><div class="layerobject_detail__content__data__hr"></div><span class="layerobject_detail__content__data__key">Наименование объекта</span><span class="layerobject_detail__content__data__value layerobject_detail__content__data--title">Здание манежа (экзерциргауса) лейб-гвардии Измайловского полка</span><div class="layerobject_detail__content__data__hr"></div><span class="layerobject_detail__content__data__key">Время возникновения объекта, основных перестроек</span><span class="layerobject_detail__content__data__value layerobject_detail__content__data--text">1795-1797</span><div class="layerobject_detail__content__data__hr"></div><span class="layerobject_detail__content__data__key">Местонахождение объекта</span><span class="layerobject_detail__content__data__value layerobject_detail__content__data--address">1-я Красноармейская ул., 13; Измайловский пр., 2-а</span><div class="layerobject_detail__content__data__hr"></div><span class="layerobject_detail__content__data__key">Категория историко-культурного значения объекта</span><span class="layerobject_detail__content__data__value layerobject_detail__content__data--text">объект культурного наследия регионального значения</span><div class="layerobject_detail__content__data__hr"></div><span class="layerobject_detail__content__data__key">Наименование и реквизиты нормативно-правового акта органа государственной власти о постановке объекта культурного наследия на государственную охрану</span><span class="layerobject_detail__content__data__value layerobject_detail__content__data--text">Закон <span class="nobr">Санкт-Петербурга</span> № 141-47 от 02.07.1997</span><div class="layerobject_detail__content__data__hr"></div><span class="layerobject_detail__content__data__key">Вид объекта</span><span class="layerobject_detail__content__data__value layerobject_detail__content__data--text">Памятник</span></div>"""
        kgiop_dict_sample = {'Наименование ансамбля': '—', 'Наименование объекта': 'Здание манежа (экзерциргауса) лейб-гвардии Измайловского полка', 'Время возникновения объекта, основных перестроек': '1795-1797', 'Местонахождение объекта': '1-я Красноармейская ул., 13; Измайловский пр., 2-а', 'Категория историко-культурного значения объекта': 'объект культурного наследия регионального значения', 'Наименование и реквизиты нормативно-правового акта органа государственной власти о постановке объекта культурного наследия на государственную охрану': 'Закон Санкт-Петербурга № 141-47 от 02.07.1997', 'Вид объекта': 'Памятник'}

        tag = BeautifulSoup(content_data, "html.parser")
        kgiop_dict = get_kgiop_dict(tag)

        self.assertEqual(kgiop_dict_sample, kgiop_dict)
