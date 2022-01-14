import os
import requests

from dotenv import load_dotenv
from fetch_xkcd_comics import get_random_comics
from file_handler import get_filename, download_image


class VkApiError(Exception):
    pass


def check_vk_response(response):
    if 'error' in response:
        raise VkApiError(f"Error code is {response['error']['error_code']}. "
                         f"{response['error']['error_msg']}")


def get_vk_upload_url(group_id, token):
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
    response = response.json()
    check_vk_response(response)
    return response['response']['upload_url']


def upload_photo_to_server(upload_url, photo_path):
    with open(photo_path, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url, files=files)

    response.raise_for_status()
    response = response.json()
    check_vk_response(response)

    server = response['server']
    photo = response['photo']
    photo_hash = response['hash']

    return server, photo, photo_hash


def save_vk_wall_photo(group_id, server, photo, photo_hash, token):
    method = 'photos.saveWallPhoto'
    app_version = '5.131'
    url = f'https://api.vk.com/method/{method}'
    params = {
        'group_id': group_id,
        'server': server,
        'photo': photo,
        'hash': photo_hash,
        'access_token': token,
        'group_id': group_id,
        'v': app_version,
    }

    response = requests.post(url, params=params)
    response.raise_for_status()

    response = response.json()
    check_vk_response(response)
    owner_id = response['response'][0]['owner_id']
    media_id = response['response'][0]['id']
    return owner_id, media_id


def publish_vk_comics(group_id,
                      owner_id,
                      media_id,
                      token,
                      image_title=None):

    method = 'wall.post'
    app_version = '5.131'
    url = f'https://api.vk.com/method/{method}'
    params = {
        'owner_id': f'-{group_id}',
        'from_group': 1,
        'attachments': f'photo{owner_id}_{media_id}',
        'message': image_title,
        'access_token': token,
        'v': app_version,
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    response = response.json()
    check_vk_response(response)
    return response


def main():
    load_dotenv()
    vk_token = os.getenv('VK_ACCESS_TOKEN')
    group_id = os.getenv('VK_GROUP_ID')

    image_url, image_title = get_random_comics()
    image_name = get_filename(image_url)

    download_image(image_name, image_url)
    try:
        upload_url = get_vk_upload_url(group_id, vk_token)
        server, photo, photo_hash = upload_photo_to_server(upload_url,
                                                           image_name)

        owner_id, media_id = save_vk_wall_photo(group_id,
                                                server,
                                                photo,
                                                photo_hash,
                                                vk_token)

        publish_vk_comics(group_id, owner_id, media_id, vk_token, image_title)

    finally:
        os.remove(image_name)


if __name__ == '__main__':
    main()
