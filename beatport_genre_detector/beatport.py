import os
import requests
from bs4 import BeautifulSoup
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TIT2

MUSIC_DIR = "/Users/admin/Music/yandex.music/House"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def parse_filename(filename):
    name = os.path.splitext(filename)[0]
    if " - " in name:
        artist, track = name.split(" - ", 1)
        return artist.strip(), track.strip()
    return None, None


def search_beatport(artist, track):
    query = f"{artist} {track}"
    url = f"https://www.beatport.com/search?q={query.replace(' ', '%20')}"
    
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")

    # Ищем первый результат
    results = soup.select("li.bucket-item")

    if not results:
        return None

    first = results[0]

    # Жанр обычно есть в ссылке
    genre_tag = first.select_one(".buk-track-meta__genres")
    if genre_tag:
        return genre_tag.text.strip()

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