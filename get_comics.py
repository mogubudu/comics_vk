import os
import requests

from dotenv import load_dotenv
from fetch_xkcd_comics import get_xkcd_random_comics
from file_handler import get_filename, download_image


def get_adress_vk_wall(group_id, token=None):
    app_version = '5.131'
    method = 'photos.getWallUploadServer'
    url = f'https://api.vk.com/method/{method}'
    params = {
        'access_token': token,
        'group_id': group_id,
        'v': app_version,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
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


def vk_save_wall_photo(group_id, server, photo, hash_image, token=None):
    method = 'photos.saveWallPhoto'
    app_version = '5.131'
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
    response.raise_for_status()
    response = response.json()
    owner_id = response['response'][0]['owner_id']
    media_id = response['response'][0]['id']
    return owner_id, media_id


def public_comics_vk(group_id,
                     image_title=None,
                     owner_id=None,
                     media_id=None,
                     token=None):

    method = 'wall.post'
    app_version = '5.131'
    url = f'https://api.vk.com/method/{method}'
    params = {
        'owner_id': f'-{group_id}',
        'from_group': 1,
        'attachments': f'photo{owner_id}_{media_id}',
        'message': f'{image_title}',
        'access_token': token,
        'v': app_version,
    }

    return requests.post(url, params=params)


def main():
    load_dotenv()
    vk_token = os.getenv('VK_ACCESS_TOKEN')
    group_id = os.getenv('VK_GROUP_ID')

    image_url, image_title = get_xkcd_random_comics()
    image_name = get_filename(image_url)

    download_image(image_name, image_url)
    upload_url = get_adress_vk_wall(group_id, vk_token)
    server, photo, photo_hash = upload_photo_to_server(upload_url,
                                                       image_name)

    owner_id, media_id = vk_save_wall_photo(group_id,
                                            server,
                                            photo,
                                            photo_hash,
                                            vk_token)

    public_comics_vk(group_id, image_title, owner_id, media_id, vk_token)

    os.remove(image_name)


if __name__ == '__main__':
    main()
