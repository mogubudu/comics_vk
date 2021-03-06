import random
import requests


def get_last_comics_number():
    current_commics_url = 'https://xkcd.com/info.0.json'
    response = requests.get(current_commics_url)
    response.raise_for_status()
    last_comics_number = response.json()['num']
    return last_comics_number


def get_random_comics():
    last_comics_number = get_last_comics_number()
    random_number = random.randint(1, last_comics_number)
    url = f'https://xkcd.com/{random_number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    response = response.json()
    return response['img'], response['alt']
