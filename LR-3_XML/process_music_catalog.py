import sys
import os
from lxml import etree
import random

# Принудительно установить кодировку вывода в UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Загрузка XML и XSLT файлов
xml_file = 'music_albums.xml'
text_xslt_file = 'xml_to_text.xslt'
html_xslt_file = 'xml_to_html.xslt'

# Парсинг XML
try:
    xml_doc = etree.parse(xml_file)
except etree.ParseError as e:
    print(f"Ошибка при парсинге XML: {e}")
    exit(1)

# XSLT-преобразования
def apply_xslt(xslt_file, output_file):
    try:
        xslt_doc = etree.parse(xslt_file)
        transform = etree.XSLT(xslt_doc)
        result = transform(xml_doc)
        with open(output_file, 'wb') as f:
            f.write(result)
    except Exception as e:
        print(f"Ошибка при применении XSLT ({xslt_file}): {e}")

# Применение текстового преобразования
apply_xslt(text_xslt_file, 'music_catalog.txt')

# Применение HTML-преобразования
apply_xslt(html_xslt_file, 'music_catalog.html')

# XPath-запросы
def run_xpath_queries():
    try:
        # a) Альбомы жанра 'Рок'
        rock_albums = xml_doc.xpath("/musicCatalog/album[genres/genre='Рок']/title")
        print("Альбомы жанра Рок:", [album.text for album in rock_albums])

        # b) Жанры исполнителя 'Майкл Джексон'
        genres = xml_doc.xpath("/musicCatalog/album[artists/artist='Майкл Джексон']/genres/genre")
        print("Жанры Майкла Джексона:", [genre.text for genre in genres])

        # c) Альбомы с композициями > 5 минут
        long_track_albums = xml_doc.xpath("/musicCatalog/album[tracks/track/duration > 300]/title")
        print("Альбомы с композициями > 5 мин:", [album.text for album in long_track_albums])

        # d) Случайный плейлист из 5 композиций
        all_tracks = xml_doc.xpath("/musicCatalog/album/tracks/track/title")
        random_playlist = random.sample(all_tracks, min(5, len(all_tracks)))
        print("Случайный плейлист:", [track.text for track in random_playlist])

        # e) Собственный запрос: Альбомы с >1 жанром, возрастным ограничением '+' и суммарной длительностью >240 секунд
        custom_query = xml_doc.xpath(
            "/musicCatalog/album[count(genres/genre) > 1 and contains(ageRestriction, '+') and sum(tracks/track/duration) > 240]/title"
        )
        print("Собственный запрос (альбомы с несколькими жанрами и длинными композициями):", [album.text for album in custom_query])

    except etree.XPathEvalError as e:
        print(f"Ошибка в XPath-запросе: {e}")
    except Exception as e:
        print(f"Общая ошибка при выполнении XPath-запросов: {e}")

if __name__ == "__main__":
    run_xpath_queries()