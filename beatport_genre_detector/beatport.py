import os
import shutil
import requests
from bs4 import BeautifulSoup
import json

MUSIC_DIR = "/Users/admin/Music/yandex.music/melodic house"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "identity",
    "Accept-Language": "ru-RU,ru;q=0.9",
    "Cache-Control": "max-age=0",
    "Dnt": "1",
    "Priority": "u=0, i",
    "Sec-Ch-Ua": '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"macOS"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
}


def parse_filename(filename):
    name = os.path.splitext(filename)[0]
    if " - " in name:
        artist, track = name.split(" - ", 1)
        return artist.strip(), track.strip()
    return None, None


def search_beatport(artist, track):
    query = f"{artist} {track}"
    url = f"https://www.beatport.com/search?q={query.replace(' ', '+')}"

    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    result = soup.find("script", type="application/json", id="__NEXT_DATA__")

    if not result:
        return None

    script_text = json.loads(result.contents[0])

    try:
        genre_tag = script_text['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['tracks']['data'][0]['genre'][0]['genre_name']
    except Exception:
        genre_tag = None

    return genre_tag


def move_to_genre_folder(filepath, genre):
    """
    Перемещает файл в подпапку с названием жанра внутри MUSIC_DIR.
    Возвращает новый путь к файлу или None при ошибке.
    """
    # Очищаем название жанра от символов, недопустимых в именах папок
    safe_genre = genre.strip().replace("/", "-").replace("\\", "-").replace(":", "-").lower()

    genre_dir = os.path.join(MUSIC_DIR, safe_genre)
    os.makedirs(genre_dir, exist_ok=True)

    filename = os.path.basename(filepath)
    dest_path = os.path.join(genre_dir, filename)

    # Если файл с таким именем уже существует — добавляем суффикс
    if os.path.exists(dest_path):
        base, ext = os.path.splitext(filename)
        dest_path = os.path.join(genre_dir, f"{base}_1{ext}")

    shutil.move(filepath, dest_path)
    return dest_path


def process_files():
    moved = 0
    skipped = 0
    not_found = 0

    for file in os.listdir(MUSIC_DIR):
        # if not file.lower().endswith(".mp3"):
        #     continue

        artist, track = parse_filename(file)
        if not artist or not track:
            print(f"❌ Пропущен (неверное имя): {file}")
            skipped += 1
            continue

        print(f"🔍 Ищем: {artist} - {track}")

        genre = search_beatport(artist, track)

        if genre:
            filepath = os.path.join(MUSIC_DIR, file)
            # set_genre(filepath, genre)
            print(f"✅ {file} → {genre}")
        else:
            print(f"⚠️ Не найдено: {file}")

        # if genre:
        #     filepath = os.path.join(MUSIC_DIR, file)
            new_path = move_to_genre_folder(filepath, genre)
        #     print(f"✅ {file} → [{genre}] {new_path}")
        #     moved += 1
        # else:
        #     print(f"⚠️ Жанр не найден: {file}")
        #     not_found += 1

    print(f"\n📊 Итог: перемещено {moved}, пропущено {skipped}, не найдено {not_found}")


if __name__ == "__main__":
    process_files()