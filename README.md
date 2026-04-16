# Beatport genre detector

Скрипт находится в файле `beatport.py`
Скрипт показывающий жанр трека. Жанр получает по имени артиста и названию трека.
Формат наименования должен быть следующим {Имя артиста} - {Название трека}.{расширение(.mp3/.flac./.aiff)}

Для работы необходим установленный PYTHON 3. Плюс необходимо скачать зависимости:
1. requests: `pip3 install requests`
2. Beatifulsoap `pip3 install beautifulsoup4`
Если команда `pip3` не найдена, но можно попробовать `pip`

На 8й строке скрипта необходимо указать путь к папке с треками:

Вместо `MUSIC_DIR = "/Users/admin/Music/yandex.music/House"` 
указать (например, для windows): `MUSIC_DIR = "C:\Users\mlazarev\Desktop\LESSONS\music\techno"`
![Alt text](/screenshots/music_dir.png)

Для запуска скрипта необходимо через терминал ("Командная строка" в Windows) выполнить команду `python3 beatport.py`
![Alt text](/screenshots/execute_command.png)
