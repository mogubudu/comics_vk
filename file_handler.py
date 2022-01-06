import os
import requests
from urllib.parse import urlparse, unquote


def get_filename(url):
    path = urlparse(url).path
    path = unquote(path)
    filename = os.path.basename(path)

    filename = filename.replace(' ', '_')
    return filename


def download_image(image_name, image_url):
    response = requests.get(image_url)
    response.raise_for_status()

    with open(f'{image_name}', 'wb') as file:
        file.write(response.content)


def main():
    pass


if __name__ == '__main__':
    main()
