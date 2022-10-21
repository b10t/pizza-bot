import json
import logging

from environs import Env

from moltin_api import Moltin

logger = logging.getLogger('pizza-shop')


def load_menu(moltin_api):
    """Загружает данные меню."""
    with open('load_data/menu.json', 'r') as file_menu:
        menu_items = json.load(file_menu)

    for menu_item in menu_items:
        logger.debug(menu_item)

        image_url = menu_item.get('product_image').get('url')

        logger.debug(image_url)

        break


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG,
    )

    env = Env()
    env.read_env()

    moltin_client_id = env.str('MOLTIN_CLIENT_ID')
    moltin_client_secret = env.str('MOLTIN_CLIENT_SECRET')
    moltin_api = Moltin(moltin_client_id, moltin_client_secret)

    load_menu(moltin_api)

    # print(moltin_api.get_access_token())

    # print(moltin_api.upload_file_from_url(
    #     'https://dodopizza-a.akamaihd.net/static/Img/Products/Pizza/ru-RU/1626f452-b56a-46a7-ba6e-c2c2c9707466.jpg'))

    # print(moltin_api.get_products())


if __name__ == '__main__':
    main()
