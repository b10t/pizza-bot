import json
import logging

from environs import Env

from moltin_api import Moltin

logger = logging.getLogger('pizza-shop')


def delete_all_products(moltin_api):
    """Удаляет все товары."""
    for product in moltin_api.get_products():
        moltin_api.delete_product(product.get('id'))


def delete_all_files(moltin_api):
    """Удаляет все файлы."""
    for remote_file in moltin_api.get_files():
        moltin_api.delete_file(remote_file.get('id'))


def create_product(moltin_api, product, image_id):
    """Создаёт товар."""
    new_product = moltin_api.create_product(
        product.get('name'),
        product.get('description'),
        product.get('price')
    )

    moltin_api.add_file_to_product(new_product.get('id'), image_id)

    logger.info(product.get('name'))

    return new_product


def load_menu(moltin_api):
    """Загружает данные меню."""
    with open('load_data/menu.json', 'r') as file_menu:
        menu_items = json.load(file_menu)

    for menu_item in menu_items:
        logger.debug(menu_item)

        image_url = menu_item.get('product_image').get('url')
        logger.debug(image_url)

        upload_file = moltin_api.upload_file_from_url(image_url)
        logger.debug(upload_file)

        file_id = upload_file.get('data').get('id')
        logger.debug(file_id)

        create_product(moltin_api, menu_item, file_id)


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
    )

    env = Env()
    env.read_env()

    moltin_client_id = env.str('MOLTIN_CLIENT_ID')
    moltin_client_secret = env.str('MOLTIN_CLIENT_SECRET')
    moltin_api = Moltin(moltin_client_id, moltin_client_secret)

    # delete_all_products(moltin_api)
    # delete_all_files(moltin_api)
    # load_menu(moltin_api)

    # TODO удалить
    # print(moltin_api.get_access_token())
    # print(moltin_api.get_products())
    # print(moltin_api.get_files())
    # print(moltin_api.create_flow('Pizzeria2', 'My Pizzeria2'))
    # print(moltin_api.get_flows())
    print(moltin_api.get_flow_by_slug('Pizzeria'))



if __name__ == '__main__':
    main()
