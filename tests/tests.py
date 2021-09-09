from unittest import TestCase

from main import extract_tag_kgiop_object, flat_html, get_kgiop_dict, extract_coords


HTML_KGIOP_OBJECT_WITH_COORDS = "kgiop_object_with_coords.html"
HTML_CONTENT_DATA = "layerobject_detail__content__data.html"


class TestKgiopObjectWithCoords(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.object_id = 1
        with open(HTML_KGIOP_OBJECT_WITH_COORDS) as f:
            cls.html = f.read()

        with open(HTML_CONTENT_DATA) as f:
            cls.content_data = f.read()

        cls.kgiop_dict = {
            'Наименование ансамбля': '—',
            'Наименование объекта': 'Здание Консисторского управления Могилевской Римско-католической архиепархии с костелом Успения Девы Марии (Духовная семинария Римско-католической архиепархии)',
            'Время возникновения объекта, основных перестроек': '1870-1873; 1878-1879; 1896-1897; 1900-1902',
            'Местонахождение объекта': '1-я Красноармейская ул., 11, лит. А, Б',
            'Категория историко-культурного значения объекта': 'объект культурного наследия регионального значения',
            'Наименование и реквизиты нормативно-правового акта органа государственной власти о постановке объекта культурного наследия на государственную охрану': 'Распоряжение КГИОП № 10-22 от 21.07.2009',
            'Вид объекта': 'Памятник'
        }

        cls.coods = {'lat': '59.916595', 'lon': '30.312194'}

    def test_extract_tag_kgiop_object(self) -> None:
        tag = extract_tag_kgiop_object(self.html, self.object_id)

        self.assertEqual(self.content_data, flat_html(str(tag)))

    def test_get_kgiop_dict(self) -> None:
        tag = extract_tag_kgiop_object(self.html, self.object_id)
        kgiop_dict = get_kgiop_dict(tag)

        self.assertEqual(self.kgiop_dict, kgiop_dict)

    def test_extract_coords(self) -> None:
        coords = extract_coords(self.html, self.object_id)
        self.assertEqual(self.coods, coords)
