import time

import requests
from slugify import slugify


class Moltin():
    __moltin_token = {}
    __moltin_client_id = ''
    __moltin_client_secret = ''

    def __init__(self, moltin_client_id='', moltin_client_secret=''):
        if not self.__moltin_client_id:
            self.__moltin_client_id = moltin_client_id
            self.__moltin_client_secret = moltin_client_secret

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__.upper())

    def __eq__(self, other):
        return other is self

    def is_token_expired(self):
        """Проверка, истек ли срок действия токена."""
        if not self.__moltin_token:
            return True

        token_expires = self.__moltin_token.get('expires', 0)

        return time.time() > token_expires

    def get_access_token(self):
        """Возвращает токен."""
        if self.is_token_expired():
            if self.__moltin_client_secret:
                data = {
                    'client_id': self.__moltin_client_id,
                    'client_secret': self.__moltin_client_secret,
                    'grant_type': 'client_credentials',
                }
            else:
                data = {
                    'client_id': self.__moltin_client_id,
                    'grant_type': 'implicit',
                }

            response = requests.post(
                'https://api.moltin.com/oauth/access_token',
                data=data
            )
            response.raise_for_status()

            self.__moltin_token = response.json()

        return self.__moltin_token

    def get_or_create_cart(self, cart_id):
        """Создаёт корзину."""
        if cart := self.get_cart(cart_id):
            return cart

        moltin_token = self.get_access_token()

        headers = {
            'Authorization': f'Bearer {moltin_token.get("access_token")}'
        }

        payload = {
            'data': {
                'id': cart_id,
                'name': f'My cart ({cart_id})',
            }
        }

        response = requests.post(
            'https://api.moltin.com/v2/carts',
            headers=headers,
            json=payload
        )
        response.raise_for_status()

        return response.json()

    def get_cart(self, cart_id):
        """Получает данные корзины."""
        moltin_token = self.get_access_token()

        headers = {
            'Authorization': f'Bearer {moltin_token.get("access_token")}'
        }

        response = requests.get(
            f'https://api.moltin.com/v2/carts/{cart_id}',
            headers=headers,
        )
        response.raise_for_status()

        return response.json()

    def get_cart_items(self, cart_id):
        """Получает содержимое корзины."""
        moltin_token = self.get_access_token()

        headers = {
            'Authorization': f'Bearer {moltin_token.get("access_token")}'
        }

        response = requests.get(
            f'https://api.moltin.com/v2/carts/{cart_id}/items',
            headers=headers,
        )
        response.raise_for_status()

        return response.json()

    def add_cart_item(self, cart_id, item_id, quantity=1):
        """Добавляет товар в корзину."""
        moltin_token = self.get_access_token()

        headers = {
            'Authorization': f'Bearer {moltin_token.get("access_token")}'
        }

        payload = {
            'data': {
                'id': item_id,
                'type': 'cart_item',
                'quantity': int(quantity)
            }
        }

        response = requests.post(
            f'https://api.moltin.com/v2/carts/{cart_id}/items',
            headers=headers,
            json=payload
        )
        response.raise_for_status()

        return response.json()

    def remove_cart_item(self, cart_id, item_id):
        """Удаляет товар из корзины."""
        moltin_token = self.get_access_token()

        headers = {
            'Authorization': f'Bearer {moltin_token.get("access_token")}'
        }

        response = requests.delete(
            f'https://api.moltin.com/v2/carts/{cart_id}/items/{item_id}',
            headers=headers,
        )
        response.raise_for_status()

        return response.json()

    def create_product(self, name, description, price, currency='RUB'):
        """Создаёт товар."""
        moltin_token = self.get_access_token()

        headers = {
            'Authorization': f'Bearer {moltin_token.get("access_token")}'
        }

        payload = {
            'data': {
                'type': 'product',
                'name': f'{name}',
                'slug': f'{slugify(name)}',
                'sku':  f'{slugify(name)}-001',
                'description': description,
                'manage_stock': False,
                'price': [
                    {
                        'amount': price,
                        'currency': currency,
                        'includes_tax': True,
                    }
                ],
                'status': 'live',
                'commodity_type': 'physical',
            }
        }

        response = requests.post(
            f'https://api.moltin.com/v2/products',
            headers=headers,
            json=payload
        )
        response.raise_for_status()

        return response.json().get('data', {})

    def delete_product(self, product_id):
        """Удаляет товар."""
        moltin_token = self.get_access_token()

        headers = {
            'Authorization': f'Bearer {moltin_token.get("access_token")}'
        }

        response = requests.delete(
            f'https://api.moltin.com/v2/products/{product_id}',
            headers=headers
        )
        response.raise_for_status()

        return response.status_code

    def get_products(self):
        """Возвращает список товаров."""
        products = []
        moltin_token = self.get_access_token()

        headers = {
            'Authorization': f'Bearer {moltin_token.get("access_token")}'
        }

        response = requests.get(
            'https://api.moltin.com/v2/products',
            headers=headers
        )
        response.raise_for_status()

        products = response.json().get('data', [])

        return products

    def get_product(self, item_id):
        """Возвращает описание товара."""
        moltin_token = self.get_access_token()

        headers = {
            'Authorization': f'Bearer {moltin_token.get("access_token")}'
        }

        response = requests.get(
            f'https://api.moltin.com/v2/products/{item_id}',
            headers=headers
        )
        response.raise_for_status()

        return response.json().get('data', {})

    def add_file_to_product(self, product_id, file_id):
        """Добавляет файл к товару."""
        moltin_token = self.get_access_token()

        headers = {
            'Authorization': f'Bearer {moltin_token.get("access_token")}'
        }

        payload = {
            'data': {
                'type': 'main_image',
                'id': f'{file_id}',
            }
        }

        response = requests.post(
            f'https://api.moltin.com/v2/products/{product_id}/relationships/main-image',
            headers=headers,
            json=payload
        )
        response.raise_for_status()

        return response.json().get('data', {})

    def create_customer(self, customer_id, customer_email):
        """Создает покупателя."""
        moltin_token = self.get_access_token()

        headers = {
            'Authorization': f'Bearer {moltin_token.get("access_token")}'
        }

        payload = {
            'data': {
                'type': 'customer',
                'name': f'{customer_id}',
                'email': f'{customer_email}'
            }
        }

        response = requests.post(
            f'https://api.moltin.com/v2/customers',
            headers=headers,
            json=payload
        )
        response.raise_for_status()

        return response.json()

    def get_files(self):
        """Возвращает список файлов."""
        products = []
        moltin_token = self.get_access_token()

        headers = {
            'Authorization': f'Bearer {moltin_token.get("access_token")}'
        }

        response = requests.get(
            'https://api.moltin.com/v2/files',
            headers=headers
        )
        response.raise_for_status()

        products = response.json().get('data', [])

        return products

    def get_file_url(self, file_id):
        """Получает URL файла по id."""
        moltin_token = self.get_access_token()

        headers = {
            'Authorization': f'Bearer {moltin_token.get("access_token")}'
        }

        response = requests.get(
            f'https://api.moltin.com/v2/files/{file_id}',
            headers=headers
        )
        response.raise_for_status()

        return response.json()

    def delete_file(self, file_id):
        """Удаляет файл."""
        moltin_token = self.get_access_token()

        headers = {
            'Authorization': f'Bearer {moltin_token.get("access_token")}'
        }

        response = requests.delete(
            f'https://api.moltin.com/v2/files/{file_id}',
            headers=headers
        )
        response.raise_for_status()

        return response.status_code

    def upload_file_from_url(self, file_url):
        """Загружает файл из ссылки."""
        moltin_token = self.get_access_token()

        headers = {
            'Authorization': f'Bearer {moltin_token.get("access_token")}',
        }

        files = {
            'file_location': (None, file_url)
        }

        response = requests.post(
            'https://api.moltin.com/v2/files',
            headers=headers,
            files=files)
        response.raise_for_status()

        return response.json()

    def create_flow(self, flow_name, flow_description):
        """Создаёт Flow."""
        moltin_token = self.get_access_token()

        headers = {
            'Authorization': f'Bearer {moltin_token.get("access_token")}'
        }

        payload = {
            'data': {
                'type': 'flow',
                'name': f'{flow_name}',
                'slug': f'{slugify(flow_name)}',
                'description': flow_description,
                'enabled': True,
            }
        }

        response = requests.post(
            f'https://api.moltin.com/v2/flows',
            headers=headers,
            json=payload
        )
        response.raise_for_status()

        return response.json()

    def get_flows(self):
        """Получает список Flows."""
        moltin_token = self.get_access_token()

        headers = {
            'Authorization': f'Bearer {moltin_token.get("access_token")}'
        }

        response = requests.get(
            f'https://api.moltin.com/v2/flows',
            headers=headers,
        )
        response.raise_for_status()

        return response.json().get('data', [])

    def get_flow_by_slug(self, flow_slug):
        """Получает Flow по slug."""
        flows = self.get_flows()

        flow_slug = slugify(flow_slug)

        for flow in flows:
            if flow.get('slug') == flow_slug:
                return flow

    def create_field_in_flow(self,
                             flow_id,
                             field_name,
                             field_description,
                             field_type,
                             required=True):
        """Создаёт поле в Flow."""
        moltin_token = self.get_access_token()

        headers = {
            'Authorization': f'Bearer {moltin_token.get("access_token")}'
        }

        payload = {
            'data': {
                'type': 'field',
                'name': field_name,
                'slug': slugify(field_name),
                'field_type': field_type,
                'validation_rules': [],
                'description': field_description,
                'required': required,
                'enabled': True,
                'order': 1,
                'omit_null': False,
                'relationships': {
                    'flow': {
                        'data': {
                            'type': 'flow',
                            'id': flow_id
                        }
                    }
                }
            }
        }

        response = requests.post(
            f'https://api.moltin.com/v2/fields',
            headers=headers,
            json=payload
        )
        response.raise_for_status()

        return response.json()

    def create_entry(self, flow_name, field_data):
        """Создание записи."""
        moltin_token = self.get_access_token()

        headers = {
            'Authorization': f'Bearer {moltin_token.get("access_token")}'
        }

        payload = {
            'data': {
                'type': 'entry',
                **field_data
            }
        }

        response = requests.post(
            f'https://api.moltin.com/v2/flows/{slugify(flow_name)}/entries',
            headers=headers,
            json=payload
        )
        response.raise_for_status()

        return response.json()

    def get_entries(self, flow_name):
        """Возвращает все записи."""
        entries = []
        moltin_token = self.get_access_token()

        headers = {
            'Authorization': f'Bearer {moltin_token.get("access_token")}'
        }

        response = requests.get(
            f'https://api.moltin.com/v2/flows/{slugify(flow_name)}/entries',
            headers=headers
        )
        response.raise_for_status()

        entries = response.json().get('data', [])

        return entries

    def delete_entry(self, flow_name, entry_id):
        """Удаление записи."""
        moltin_token = self.get_access_token()

        headers = {
            'Authorization': f'Bearer {moltin_token.get("access_token")}'
        }

        response = requests.delete(
            f'https://api.moltin.com/v2/flows/{slugify(flow_name)}/entries/{entry_id}',
            headers=headers
        )
        response.raise_for_status()

        return response.status_code
