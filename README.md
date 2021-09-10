# Объекты культурного наследия

Для того чтобы выгрузить все объекты культурного наследия с сайта https://kgiop.gov.spb.ru/uchet/list_objects/  
необходимо запустить скрипт:
```shell
python main.py
```

Если скрипт необходимо запустить в фоне, то
```shell
nohup python3.8 main.py &
```

В json файле `OUTPUT_FILE = "kgiop_objects.json"`  
будет содержаться список объектов культурного наследия, которые удалось распарсить.

Резервные копии данных находятся на [google drive](https://drive.google.com/drive/folders/1VeEjJdENpMjL3JuekiWn-JfOF_wGoVc5).
Репозиторий на [github](https://github.com/aeksei/parse_kgiop).


## Логи и данные
Для того, чтобы скачать все логи и файл с объектами культурного наследия  
необходимо выполнить:
```shell
scp itmo_greenfolder:/home/pervushin/parse_kgiop/kgiop_objects.json kgiop_objects.json
scp -r itmo_greenfolder:/home/pervushin/parse_kgiop/logs logs
scp itmo_greenfolder:/home/pervushin/parse_kgiop/nohup.out nohup.out
```

Для очистки логов необходимо выполнить:
```shell
rm -rf logs/ && rm nohup.out
```


## Regex
Здесь находится регулярное выражение, которое парсит координаты объекта  
https://regex101.com/r/l6ipwx/1
