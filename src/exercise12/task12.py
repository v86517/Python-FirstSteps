import asyncio
import os
from prettytable import PrettyTable
import requests
from aioconsole import ainput

class Downloader:
    def __init__(self, url, directory):
        self.url = url
        self.directory = directory
        self.status = None

    def download(self):
        try:
            response = requests.get(self.url, timeout=10)
            if response.status_code == 200:
                data = response.content
                filename = os.path.basename(self.url)
                if not filename:
                    filename = 'image_' + str(abs(hash(self.url))) + '.jpg'
                filepath = os.path.join(self.directory, filename)
                with open(filepath, 'wb') as f:
                    f.write(data)
                self.status = 'Успех'
            else:
                self.status = 'Ошибка'
        except PermissionError:
            self.status = 'Ошибка (нет доступа)'
        except Exception:
            self.status = 'Ошибка'


async def download_image_async(url, directory, results):
    downloader = Downloader(url, directory)
    await asyncio.to_thread(downloader.download)
    results[url] = downloader.status

async def main():
    while True:
        directory = input('Сохранить изображение в директорию: ').strip()
        if os.path.isdir(directory) and os.access(directory, os.W_OK):
            break
        else:
            print('Некорректный путь или нет доступа:')

    print('Введите ссылки на изображения (пустая строка для завершения):')
    urls = []
    tasks = []
    results = {}
    url = input().strip()
    while True:
        if not url:
            break
        urls.append(url)
        task = asyncio.create_task(download_image_async(url, directory, results))
        tasks.append(task)
        url = await ainput()

    print('Идет скачивание файлов')
    await asyncio.gather(*tasks)

    table = PrettyTable()
    table.field_names = ['Ссылка', 'Статус']
    for url in urls:
        table.add_row([url, results.get(url, "Ошибка")])
    print(table)

if __name__ == "__main__":
    asyncio.run(main())
