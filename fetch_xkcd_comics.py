import random
import requests


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
    response.raise_for_status()
    response = response.json()
    return response['img'], response['alt']


def main():
    pass


if __name__ == '__main__':
    main()
