import os
import requests
from time import sleep
import json
from datetime import datetime

def download_file(file_name, url, save_path, curpath, subfolder):
    if subfolder == 1:
        file_path = os.path.join(save_path, curpath, os.path.splitext(file_name)[0], file_name)
    else:
        file_path = os.path.join(save_path, curpath, file_name)
    if os.path.exists(file_path):
        pass
    else:
        download_response = requests.get(url)
        if subfolder == 1:
            os.makedirs(os.path.join(save_path, curpath, os.path.splitext(file_name)[0]), exist_ok=True)
        else:
            os.makedirs(os.path.join(save_path, curpath, exist_ok=True))
        with open(file_path, "wb") as f:
            f.write(download_response.content)
        print(f'[{datetime.now().strftime("%d.%m.%Y %H:%M:%S")}] {file_name}')

def get_files_list(yandex_link, save_path, curpath, subfolder):
    url = f'https://cloud-api.yandex.net/v1/disk/public/resources?public_key={yandex_link}'
    response = requests.get(url).json()
    response = response["_embedded"]["items"]
    for file in response:
        if file["type"] == "dir":
            new_curpath = os.path.join(curpath, file["name"])
            try:
                child_link = file["public_url"]
            except KeyError:
                print(f'Папка {file["name"]} не является публичной. Пропускаем.')
                continue
            get_files_list(child_link, save_path, new_curpath, subfolder)
        elif file["type"] == "file":
            download_url = file["file"]
            file_name = file["name"]
            download_file(file_name, download_url, save_path, curpath, subfolder)
            
with open('settings.json') as f:
    settings = json.load(f)
curpath = ''
save_path = settings["path"]
subfolder = settings["subfolder"]

now_time = datetime.now().strftime("%d.%m.%Y %H:%M")
print(f'Программа успешно запущена! Время: {now_time}')
print(f'Текущий путь для сохранения файлов: {save_path}')
print("--------------------------------------------------")
while True:
    get_files_list(settings["yandex_url"], save_path, curpath, subfolder)
    sleep(60)