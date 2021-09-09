import unittest

from main import extract_tag_kgiop_object, flat_html, get_kgiop_dict, extract_coords


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
