import os
import requests
import random

from dotenv import load_dotenv
from urllib.parse import urlparse, unquote


def get_filename(url):
    path = urlparse(url).path
    path = unquote(path)
    filename = os.path.basename(path)

    filename = filename.replace(' ', '_')
    return filename


def download_image(image_name, image_url, path_to_save='images/'):
    response = requests.get(image_url)
    response.raise_for_status()

    with open(f'{path_to_save}{image_name}', 'wb') as file:
        file.write(response.content)


def get_xkcd_last_comics():
    current_commics_url = 'https://xkcd.com/info.0.json'
    response = requests.get(current_commics_url)
    response.raise_for_status()
    last_comics_number = response.json()['num']
    return last_comics_number


def get_xkcd_random_comics():
    last_comics_number = get_xkcd_last_comics()
    random_number = random.randint(1, last_comics_number)
    url = f'https://xkcd.com/{random_number}/info.0.json'
    response = requests.get(url)
    response = response.json()
    return response['img'], response['alt']


def get_adress_vk_wall(token=None):
    app_version = '5.131'
    method = 'photos.getWallUploadServer'
    group_id = 209846789
    url = f'https://api.vk.com/method/{method}'
    params = {
        'access_token': token,
        'group_id': group_id,
        'v': app_version,
    }

    response = requests.get(url, params=params)
    return response.json()['response']['upload_url']


def upload_photo_to_server(upload_url, path_to_photo):
    with open(path_to_photo, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
        server = response.json()['server']
        photo = response.json()['photo']
        photo_hash = response.json()['hash']

        return server, photo, photo_hash


def vk_save_wall_photo(server, photo, hash_image, token=None):
    method = 'photos.saveWallPhoto'
    app_version = '5.131'
    group_id = 209846789
    url = f'https://api.vk.com/method/{method}'
    params = {
        'group_id': group_id,
        'server': server,
        'photo': photo,
        'hash': hash_image,
        'access_token': token,
        'group_id': group_id,
        'v': app_version,
    }

    response = requests.post(url, params=params)
    response = response.json()
    owner_id = response['response'][0]['owner_id']
    media_id = response['response'][0]['id']
    return owner_id, media_id


def public_comics_vk(image_title=None,
                     owner_id=None,
                     media_id=None,
                     token=None):

    method = 'wall.post'
    app_version = '5.131'
    group_id = 209846789
    url = f'https://api.vk.com/method/{method}'
    params = {
        'owner_id': f'-{group_id}',
        'from_group': 1,
        'attachments': f'photo{owner_id}_{media_id}',
        'message': f'{image_title}',
        'access_token': token,
        'v': app_version,
    }

    requests.post(url, params=params)


def main():
    load_dotenv()

    vk_token = os.getenv('VK_ACCESS_TOKEN')
    image_url, image_title = get_xkcd_random_comics()
    image_name = get_filename(image_url)

    download_image(image_name, image_url)
    upload_url = get_adress_vk_wall(vk_token)
    server, photo, photo_hash = upload_photo_to_server(upload_url,
                                                       f'images/{image_name}')

    owner_id, media_id = vk_save_wall_photo(server,
                                            photo,
                                            photo_hash,
                                            vk_token)

    public_comics_vk(image_title, owner_id, media_id, vk_token)
    os.remove(f'images/{image_name}')


if __name__ == '__main__':
    main()
