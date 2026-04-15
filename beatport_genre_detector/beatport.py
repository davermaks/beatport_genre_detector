import os
import requests
from bs4 import BeautifulSoup
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TIT2
import json

MUSIC_DIR = "/Users/admin/Music/yandex.music/House"

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
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
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

    # Ищем первый результат
    # results = soup.select("li.bucket-item")
    result = soup.find("script", type="application/json", id="__NEXT_DATA__")

    if not result:
        return None
    
    script_text = json.loads(result.contents[0])

    # scores = result.select('["score"]:')
    # Жанр обычно есть в ссылке
    genre_tag = script_text['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['tracks']['data'][0]['genre'][0]['genre_name']
    if genre_tag:
        return genre_tag

    return None


def set_genre(filepath, genre):
    try:
        audio = EasyID3(filepath)
    except:
        audio = ID3()

    audio["genre"] = genre
    audio.save(filepath)


def process_files():
    for file in os.listdir(MUSIC_DIR):
        if not file.lower().endswith(".mp3"):
            continue

        artist, track = parse_filename(file)
        if not artist or not track:
            print(f"❌ Пропущен: {file}")
            continue

        print(f"🔍 Ищем: {artist} - {track}")

        genre = search_beatport(artist, track)

        if genre:
            filepath = os.path.join(MUSIC_DIR, file)
            # set_genre(filepath, genre)
            print(f"✅ {file} → {genre}")
        else:
            print(f"⚠️ Не найдено: {file}")


if __name__ == "__main__":
    process_files()